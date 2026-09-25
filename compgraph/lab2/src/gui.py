import math
import os
import tkinter as tk
from tkinter import filedialog

from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from lighting import Vector, LightSource, Camera, calculate_luminance, look_at_angles, render, to_image

IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img")


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
        self.viewer_scales: dict[str, tk.Scale] = {}

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
        self.light1_enabled = tk.BooleanVar(value=True)
        tk.Checkbutton(self.left_frame, text="включен", variable=self.light1_enabled,
                       command=self.calculate).pack(anchor="w")

        self.add_section("Источник 2")
        self.add_entry("light2_x", "X, мм", "10000")
        self.add_entry("light2_y", "Y, мм", "-10000")
        self.add_entry("light2_z", "Z, мм", "2000")
        self.add_entry("light2_intensity", "I0, Вт/ср", "3000")
        self.light2_enabled = tk.BooleanVar(value=True)
        tk.Checkbutton(self.left_frame, text="включен", variable=self.light2_enabled,
                       command=self.calculate).pack(anchor="w")

        self.add_section("Модель Блинн-Фонга")
        self.add_entry("diffuse_coef", "kd (диффузная)", "0.5")
        self.add_entry("specular_coef", "ks (зеркальная)", "0.8")
        self.add_entry("shininess", "ke (блеск)", "40")

        self.add_section("Наблюдатель")
        self.add_scale("viewer_x", "x0, мм", -10000, 10000, 0)
        self.add_scale("viewer_y", "y0, мм", -10000, 10000, 0)
        self.add_scale("viewer_z", "z0, мм", -10000, 10000, 6000)
        self.add_scale("yaw", "азимут, °", -180, 180, 0, resolution=1)
        self.add_scale("pitch", "наклон, °", -90, 90, -90, resolution=1)
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

        # область для вывода изображения
        self.figure = Figure(figsize=(6, 6))
        self.axes = self.figure.add_subplot(111)
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
        entry = tk.Entry(row, width=10)
        entry.insert(0, default)
        entry.pack(side=tk.LEFT)
        entry.bind("<Return>", lambda event: self.calculate())
        self.entries[key] = entry

    def add_scale(self, key: str, text: str, min_value: int, max_value: int, default: int,
                  resolution: int = 50) -> None:
        row = tk.Frame(self.left_frame)
        row.pack(fill=tk.X)
        tk.Label(row, text=text, width=10, anchor="w").pack(side=tk.LEFT)
        scale = tk.Scale(row, from_=min_value, to=max_value, resolution=resolution, orient=tk.HORIZONTAL,
                         length=200)
        scale.set(default)
        # пересчитываем, только когда ползунок отпущен
        scale.bind("<ButtonRelease-1>", lambda event: self.calculate())
        scale.pack(side=tk.LEFT)
        self.viewer_scales[key] = scale

    def on_look_at_toggle(self) -> None:
        # в режиме слежения за сферой углы вычисляются автоматически
        state = tk.DISABLED if self.look_at_sphere.get() else tk.NORMAL
        self.viewer_scales["yaw"].config(state=state)
        self.viewer_scales["pitch"].config(state=state)
        self.calculate()

    def set_scale(self, key: str, value: float) -> None:
        # выключенный ползунок игнорирует set, поэтому временно включаем его
        scale = self.viewer_scales[key]
        state = scale.cget("state")
        scale.config(state=tk.NORMAL)
        scale.set(round(value))
        scale.config(state=state)

    def get_float(self, key: str) -> float:
        return float(self.entries[key].get().replace(",", "."))

    def show_info(self, text: str, color: str = "black") -> None:
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, text)
        self.info_text.config(state=tk.DISABLED, fg=color)

    def calculate(self) -> None:
        try:
            width = self.get_float("width")
            height = self.get_float("height")
            width_resolution = int(self.get_float("width_resolution"))
            center = Vector(self.get_float("center_x"), self.get_float("center_y"), self.get_float("center_z"))
            radius = self.get_float("radius")
            diffuse_coef = self.get_float("diffuse_coef")
            specular_coef = self.get_float("specular_coef")
            shininess = self.get_float("shininess")
            viewer = Vector(float(self.viewer_scales["viewer_x"].get()),
                            float(self.viewer_scales["viewer_y"].get()),
                            float(self.viewer_scales["viewer_z"].get()))
            yaw = float(self.viewer_scales["yaw"].get())
            pitch = float(self.viewer_scales["pitch"].get())
            screen_distance = self.get_float("screen_distance")

            light1 = LightSource(self.get_float("light1_x"), self.get_float("light1_y"),
                                 self.get_float("light1_z"), self.get_float("light1_intensity"))
            light2 = LightSource(self.get_float("light2_x"), self.get_float("light2_y"),
                                 self.get_float("light2_z"), self.get_float("light2_intensity"))
        except ValueError:
            self.show_info("Ошибка: все параметры должны быть числами", "red")
            return

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
            self.set_scale("yaw", yaw)
            self.set_scale("pitch", pitch)
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

        # нормировка на максимальное значение (0-255)
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
        self.axes.set_title("Распределение яркости (0-255)")
        # оси графика - координаты на экране камеры, а не мировые X и Y
        self.axes.set_xlabel("u (вправо по экрану), мм")
        self.axes.set_ylabel("v (вверх по экрану), мм")
        self.draw_world_axes(camera)
        self.canvas.draw()

    def draw_world_axes(self, camera: Camera) -> None:
        """Значок ориентации: проекции мировых осей X, Y, Z на плоскость экрана."""
        origin = (0.12, 0.12)  # в долях области графика
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
