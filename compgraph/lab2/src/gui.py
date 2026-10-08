import math
import os
import tkinter as tk
from tkinter import filedialog

from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from lighting import Vector, LightSource, Camera, calculate_luminance, look_at_angles, render, to_image

IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img")
AUTO_CALCULATE_DELAY_MS = 700  # пауза после ввода, после которой запускается пересчет


def check_range(warnings: list[str], name: str, value: float, low: float, high: float) -> None:
    if value < low or value > high:
        warnings.append(f"{name} = {value:g} вне рекомендуемого диапазона [{low:g}; {high:g}]")


def format_point(point: Vector) -> str:
    return f"({point.x:8.1f}, {point.y:8.1f}, {point.z:8.1f})"


def point_info(name: str,
               point: Vector,
               viewer: Vector,
               center: Vector,
               lights: list[LightSource],
               diffuse_coef: float,
               specular_coef: float,
               shininess: float) -> str:
    """Яркость в одной заданной точке сферы."""
    normal = (point - center).normalize()
    # точка видна наблюдателю, если нормаль "смотрит" в его сторону
    if (viewer - point).dot(normal) <= 0:
        return f"{name} {format_point(point)}: точка не видна наблюдателю\n"
    luminance = calculate_luminance(point, normal, viewer, lights,
                                    diffuse_coef, specular_coef, shininess)
    return f"{name} {format_point(point)}: L = {luminance:.4f} Вт/(м²·ср)\n"


class App:
    def __init__(self) -> None:
        self.last_image: list[list[int]] | None = None  # последнее изображение для сохранения
        self.entries: dict[str, tk.Entry] = {}
        self.entry_vars: list[tk.StringVar] = []  # ссылки на переменные полей
        self.defaults: dict[str, str] = {}  # значения по умолчанию
        self.pending_calculation: str | None = None  # отложенный пересчет
        self.updating_fields = False  # поля, которым пересчет не нужен

        self.root = tk.Tk()
        self.root.title("ЛР 2. Яркость на сфере от точечных источников света")

        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.add_section("Экран")
        self.add_entry("width", "Ширина W, мм", "5000")
        self.add_entry("height", "Высота H, мм", "5000")
        self.add_entry("width_resolution", "Разрешение по ширине, пикс", "500")
        self.height_resolution_label = tk.Label(self.left_frame, text="Разрешение по высоте, пикс = ?",
                                                anchor="w")
        self.height_resolution_label.pack(anchor="w")

        self.add_section("Сфера")
        self.add_entry("center_x", "Центр X, мм", "0")
        self.add_entry("center_y", "Центр Y, мм", "0")
        self.add_entry("center_z", "Центр Z, мм", "800")
        self.add_entry("radius", "Радиус R, мм", "800")

        self.add_section("Источник 1")
        self.add_entry("light1_x", "X, мм", "-10000")
        self.add_entry("light1_y", "Y, мм", "10000")
        self.add_entry("light1_z", "Z, мм", "4000")
        self.add_entry("light1_intensity", "I0, Вт/ср", "2000")
        self.add_vector_entry("light1_dir", "Направление (x, y, z)", ("0", "0", "-1"))
        self.light1_enabled = tk.BooleanVar(value=True)
        tk.Checkbutton(self.left_frame, text="включен", variable=self.light1_enabled,
                       command=self.calculate).pack(anchor="w")

        self.add_section("Источник 2")
        self.add_entry("light2_x", "X, мм", "10000")
        self.add_entry("light2_y", "Y, мм", "-10000")
        self.add_entry("light2_z", "Z, мм", "2000")
        self.add_entry("light2_intensity", "I0, Вт/ср", "3000")
        self.add_vector_entry("light2_dir", "Направление (x, y, z)", ("0", "0", "-1"))
        self.light2_enabled = tk.BooleanVar(value=True)
        tk.Checkbutton(self.left_frame, text="включен", variable=self.light2_enabled,
                       command=self.calculate).pack(anchor="w")

        self.add_section("Модель Блинн-Фонга")
        self.add_entry("diffuse_coef", "kd (диффузная)", "0.5")
        self.add_entry("specular_coef", "ks (зеркальная)", "0.8")
        self.add_entry("shininess", "ke (блеск)", "40")

        self.add_section("Наблюдатель")
        self.add_entry("viewer_x", "x0, мм", "0")
        self.add_entry("viewer_y", "y0, мм", "0")
        self.add_entry("viewer_z", "z0, мм", "6000")
        self.add_entry("yaw", "Азимут, °", "0")
        self.add_entry("pitch", "Наклон, °", "-90")
        self.add_entry("screen_distance", "Расстояние до экрана, мм", "6000")
        self.look_at_sphere = tk.BooleanVar(value=False)
        tk.Checkbutton(self.left_frame, text="смотреть на центр сферы", variable=self.look_at_sphere,
                       command=self.on_look_at_toggle).pack(anchor="w")

        buttons_frame = tk.Frame(self.left_frame)
        buttons_frame.pack(fill=tk.X, pady=6)
        tk.Button(buttons_frame, text="Рассчитать",
                  command=self.calculate).pack(side=tk.LEFT, padx=2)
        tk.Button(buttons_frame, text="Сохранить изображение",
                  command=self.save_image).pack(side=tk.LEFT, padx=2)
        tk.Button(buttons_frame, text="Сбросить",
                  command=self.reset).pack(side=tk.LEFT, padx=2)

        # область для вывода изображения
        self.figure = Figure(figsize=(6, 6), facecolor="black")
        self.axes = self.figure.add_axes((0.0, 0.0, 1.0, 1.0))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # область для вывода численных результатов
        self.info_text = tk.Text(self.right_frame, height=14, width=80, font=("Consolas", 9))
        self.info_text.pack(fill=tk.X)

    def add_section(self, title: str) -> None:
        label = tk.Label(self.left_frame, text=title, font=("Arial", 10, "bold"))
        label.pack(anchor="w", pady=(6, 0))

    def add_entry(self, key: str, text: str, default: str) -> None:
        row = tk.Frame(self.left_frame)
        row.pack(fill=tk.X)
        tk.Label(row, text=text, width=24, anchor="w").pack(side=tk.LEFT)
        self.make_entry(row, key, default, 10).pack(side=tk.LEFT)

    def make_entry(self, parent: tk.Frame, key: str, default: str, width: int) -> tk.Entry:
        var = tk.StringVar(value=default)
        var.trace_add("write", lambda *args: self.schedule_calculate())
        entry = tk.Entry(parent, width=width, textvariable=var)
        entry.bind("<Return>", lambda event: self.calculate())
        self.entry_vars.append(var)
        self.entries[key] = entry
        self.defaults[key] = default
        return entry

    def add_vector_entry(self, key: str, text: str, defaults: tuple[str, str, str]) -> None:
        row = tk.Frame(self.left_frame)
        row.pack(fill=tk.X)
        tk.Label(row, text=text, width=24, anchor="w").pack(side=tk.LEFT)
        for axis, default in zip("xyz", defaults):
            self.make_entry(row, f"{key}_{axis}", default, 5).pack(side=tk.LEFT, padx=(0, 2))

    def get_vector(self, key: str) -> Vector:
        return Vector(self.get_float(f"{key}_x"), self.get_float(f"{key}_y"), self.get_float(f"{key}_z"))

    def schedule_calculate(self) -> None:
        if self.updating_fields:
            return
        if self.pending_calculation is not None:
            self.root.after_cancel(self.pending_calculation)
        self.pending_calculation = self.root.after(AUTO_CALCULATE_DELAY_MS, self.calculate)

    def set_entry(self, key: str, value: str) -> None:
        entry = self.entries[key]
        state = entry.cget("state")
        self.updating_fields = True
        entry.config(state=tk.NORMAL)
        entry.delete(0, tk.END)
        entry.insert(0, value)
        entry.config(state=state)
        self.updating_fields = False

    def update_angle_entries_state(self) -> None:
        # в режиме слежения за сферой углы вычисляются автоматически и вручную не меняются
        state = tk.DISABLED if self.look_at_sphere.get() else tk.NORMAL
        self.entries["yaw"].config(state=state)
        self.entries["pitch"].config(state=state)

    def on_look_at_toggle(self) -> None:
        self.update_angle_entries_state()
        self.calculate()

    def reset(self) -> None:
        self.light1_enabled.set(True)
        self.light2_enabled.set(True)
        self.look_at_sphere.set(False)
        self.update_angle_entries_state()
        for key in self.entries:
            self.set_entry(key, self.defaults[key])
        self.calculate()

    def get_float(self, key: str) -> float:
        return float(self.entries[key].get().replace(",", "."))

    def show_info(self, text: str, color: str = "black") -> None:
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, text)
        self.info_text.config(state=tk.DISABLED, fg=color)

    def calculate(self) -> None:
        if self.pending_calculation is not None:
            self.root.after_cancel(self.pending_calculation)
            self.pending_calculation = None

        try:
            width = self.get_float("width")
            height = self.get_float("height")
            width_resolution = int(self.get_float("width_resolution"))
            center = Vector(self.get_float("center_x"), self.get_float("center_y"), self.get_float("center_z"))
            radius = self.get_float("radius")
            diffuse_coef = self.get_float("diffuse_coef")
            specular_coef = self.get_float("specular_coef")
            shininess = self.get_float("shininess")
            viewer = self.get_vector("viewer")
            yaw = self.get_float("yaw")
            pitch = self.get_float("pitch")
            screen_distance = self.get_float("screen_distance")

            light_params = [(self.get_vector(f"light{number}"),
                             self.get_float(f"light{number}_intensity"),
                             self.get_vector(f"light{number}_dir")) for number in (1, 2)]
        except ValueError:
            self.show_info("Ошибка: все параметры должны быть числами", "red")
            return

        if any(direction.length() == 0 for _, _, direction in light_params):
            self.show_info("Ошибка: вектор направления источника не может быть нулевым", "red")
            return
        light1, light2 = [LightSource(position.x, position.y, position.z, intensity, direction)
                          for position, intensity, direction in light_params]

        lights: list[LightSource] = []
        if self.light1_enabled.get():
            lights.append(light1)
        if self.light2_enabled.get():
            lights.append(light2)

        # проверки параметров
        if width <= 0 or height <= 0 or radius <= 0 or screen_distance <= 0:
            self.show_info("Ошибка: ширина, высота, радиус и расстояние до экрана "
                           "должны быть положительными", "red")
            return
        if (viewer - center).length() <= radius:
            self.show_info("Ошибка: наблюдатель находится внутри сферы", "red")
            return

        if self.look_at_sphere.get():
            yaw, pitch = look_at_angles(viewer, center)
            self.set_entry("yaw", f"{yaw:.1f}")
            self.set_entry("pitch", f"{pitch:.1f}")
        camera = Camera(viewer, yaw, pitch, screen_distance)
        if width_resolution <= 0:
            self.show_info("Ошибка: разрешение должно быть положительным", "red")
            return
        pixel_size = width / width_resolution
        height_resolution = int(round(height / pixel_size))
        self.height_resolution_label.config(
            text=f"Разрешение по высоте, пикс = {height_resolution}\n(1 пиксель = {pixel_size:.2f} мм)")
        if (width_resolution < 200 or width_resolution > 800
                or height_resolution < 200 or height_resolution > 800):
            self.show_info(f"Ошибка: разрешение {width_resolution} x {height_resolution} "
                           f"должно быть в диапазоне 200..800 пикселей\n"
                           f"(Разрешение по высоте вычисляется из ширины, высоты и разрешения "
                           f"по ширине, чтобы пиксели были квадратными)",
                           "red")
            return

        warnings: list[str] = []
        check_range(warnings, "W", width, 100, 10000)
        check_range(warnings, "H", height, 100, 10000)
        check_range(warnings, "xC", center.x, -10000, 10000)
        check_range(warnings, "yC", center.y, -10000, 10000)
        check_range(warnings, "zC", center.z, 100, 10000)
        check_range(warnings, "Наклон камеры", pitch, -90, 90)
        for number, light in enumerate([light1, light2], start=1):
            check_range(warnings, f"xL{number}", light.position.x, -10000, 10000)
            check_range(warnings, f"yL{number}", light.position.y, -10000, 10000)
            check_range(warnings, f"zL{number}", light.position.z, 100, 10000)
            check_range(warnings, f"I0 источника {number}", light.intensity, 0.01, 10000)
        if len(lights) == 0:
            warnings.append("Все источники выключены")

        # расчет
        self.show_info("Идет расчет...")
        self.root.update_idletasks()  # чтобы надпись появилась до начала долгого расчета
        luminance, sphere_points, height_real = render(
            width, height, width_resolution, camera, center, radius, lights,
            diffuse_coef, specular_coef, shininess)

        # поиск максимальной и минимальной яркости среди пикселей сферы
        max_luminance = -1.0
        min_luminance = math.inf
        max_point = None
        min_point = None
        for row in range(height_resolution):
            for col in range(width_resolution):
                point = sphere_points[row][col]
                if point is None:
                    continue
                if luminance[row][col] > max_luminance:
                    max_luminance = luminance[row][col]
                    max_point = point
                if luminance[row][col] < min_luminance:
                    min_luminance = luminance[row][col]
                    min_point = point

        text = (f"Разрешение: {width_resolution} x {height_resolution}, "
                f"размер пикселя {pixel_size:.2f} мм\n")
        forward = camera.forward
        text += (f"Камера: азимут {yaw:.1f}°, наклон {pitch:.1f}°, "
                 f"направление взгляда ({forward.x:.3f}, {forward.y:.3f}, {forward.z:.3f})\n")
        if max_point is not None and min_point is not None:
            text += f"Максимальная яркость: {max_luminance:.4f} Вт/(м²·ср) в точке {format_point(max_point)}\n"
            text += f"Минимальная яркость:  {min_luminance:.4f} Вт/(м²·ср) в точке {format_point(min_point)}\n"
        else:
            text += "Сфера не попадает на экран\n"

        # нормировка на максимальное значение
        image = to_image(luminance, max_luminance)

        # яркость в трех точках сферы
        text += "\nЯркость в трех точках сферы (координаты в мм):\n"
        point1 = center + Vector(0.0, 0.0, 1.0) * radius
        point2 = center + Vector(1.0, 0.0, 1.0).normalize() * radius
        point3 = center + Vector(-1.0, -1.0, 1.0).normalize() * radius
        text += point_info("Точка 1", point1, viewer, center, lights, diffuse_coef, specular_coef, shininess)
        text += point_info("Точка 2", point2, viewer, center, lights, diffuse_coef, specular_coef, shininess)
        text += point_info("Точка 3", point3, viewer, center, lights, diffuse_coef, specular_coef, shininess)

        if len(warnings) > 0:
            text += "\nПредупреждения:\n"
            for warning in warnings:
                text += "  - " + warning + "\n"

        self.show_info(text, "red" if len(warnings) > 0 else "black")
        self.last_image = image

        # вывод изображения
        self.axes.clear()
        self.axes.imshow(image, cmap="gray", vmin=0, vmax=255,
                         extent=(-width / 2, width / 2, -height_real / 2, height_real / 2))
        self.axes.set_axis_off()
        self.draw_world_axes(camera)
        self.canvas.draw()

    def draw_world_axes(self, camera: Camera) -> None:
        origin = (0.08, 0.08)  # в долях области графика
        arrow_length = 0.08
        world_axes = [("X", Vector(1.0, 0.0, 0.0), "red"),
                      ("Y", Vector(0.0, 1.0, 0.0), "lime"),
                      ("Z", Vector(0.0, 0.0, 1.0), "deepskyblue")]
        for name, axis, color in world_axes:
            du = axis.dot(camera.right)
            dv = axis.dot(camera.up)
            if math.hypot(du, dv) < 0.05:
                # ось почти параллельна взгляду: точка - ось направлена на нас, крестик - от нас
                marker = "o" if axis.dot(camera.forward) < 0 else "x"
                self.axes.plot(*origin, marker=marker, color=color, markersize=6,
                               transform=self.axes.transAxes)
                self.axes.annotate(name, xy=origin, xycoords="axes fraction", color=color,
                                   xytext=(6, 6), textcoords="offset points")
                continue
            end = (origin[0] + du * arrow_length, origin[1] + dv * arrow_length)
            self.axes.annotate("", xy=end, xytext=origin, xycoords="axes fraction",
                               arrowprops=dict(arrowstyle="->", color=color, lw=1.5))
            self.axes.annotate(name, xy=end, xycoords="axes fraction", color=color,
                               ha="center", va="center",
                               xytext=(du * 8, dv * 8), textcoords="offset points")

    def save_image(self) -> None:
        if self.last_image is None:
            return
        os.makedirs(IMG_DIR, exist_ok=True)
        path = filedialog.asksaveasfilename(initialdir=os.path.abspath(IMG_DIR),
                                            initialfile="sphere.png",
                                            defaultextension=".png",
                                            filetypes=[("PNG", "*.png")])
        if not path:
            return

        image_height = len(self.last_image)
        image_width = len(self.last_image[0])
        pil_image = Image.new("L", (image_width, image_height))
        for row in range(image_height):
            for col in range(image_width):
                pil_image.putpixel((col, row), self.last_image[row][col])
        pil_image.save(path)

    def run(self) -> None:
        self.calculate()
        self.root.mainloop()
