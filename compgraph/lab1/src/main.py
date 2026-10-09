import os
import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def calculate():
    try:
        width_mm = float(entry_W.get())
        height_mm = float(entry_H.get())
        widthRes = int(entry_Wres.get())
        heightRes = int(entry_Hres.get())
        xL_mm = float(entry_xL.get())
        yL_mm = float(entry_yL.get())
        zL_mm = float(entry_zL.get())
        I0 = float(entry_I0.get())
        R_mm = float(entry_R.get())

        dx_mm = width_mm / widthRes
        dy_mm = height_mm / heightRes
        if abs(dx_mm - dy_mm) > 1e-6:
            raise ValueError(f"Пиксели не квадратные!\nШаг по X: {dx_mm:.4f} мм\nШаг по Y: {dy_mm:.4f} мм\n"
                             f"Пожалуйста, скорректируйте соотношение сторон или разрешение.")

        # перевод в метры
        width = width_mm / 1000.0
        height = height_mm / 1000.0
        xL = xL_mm / 1000.0
        yL = yL_mm / 1000.0
        zL = zL_mm / 1000.0
        R = R_mm / 1000.0

        x = np.linspace(-width / 2, width / 2, widthRes)
        y = np.linspace(height / 2, -height / 2, heightRes)
        xs, ys = np.meshgrid(x, y)

        r = np.sqrt((xs - xL) ** 2 + (ys - yL) ** 2 + zL ** 2)
        # вектор от Ламберта = (0, 0, -lambert.z)
        # вектор расстояния = (-lambert.x + x, -lambert.y + y), -lambert.z - 0)
        # cos theta = a * b / (len(a) * len(b))
        cosTheta = zL ** 2 / (zL * r)
        I = I0 * cosTheta
        E = I * cosTheta / (r ** 2)

        mask = (xs ** 2 + ys ** 2 <= R ** 2)
        result = np.zeros_like(E)
        result[mask] = E[mask]

        img = np.zeros_like(result)
        values = result[mask]
        if values.size > 0:
            v_max = values.max()
            v_min = values.min()
            v_mean = values.mean()

            print(f"Максимальное в круге: {v_max:.4f}")
            print(f"Минимальное в круге:  {v_min:.4f}")
            print(f"Среднее в круге:      {v_mean:.4f}")
            print("-" * 50)

            def calc_exact_E(x_pt, y_pt):
                r_dist = np.sqrt((x_pt - xL) ** 2 + (y_pt - yL) ** 2 + zL ** 2)
                c_theta = zL / r_dist
                return (I0 * c_theta ** 2) / (r_dist ** 2)

            print("Значения в 5 заданных точках:")
            print(f"1. Центр круга (0, 0):             {calc_exact_E(0, 0):.4f}")
            print(f"2. Пересечение +X ({R_mm:.0f} мм, 0):   {calc_exact_E(R, 0):.4f}")
            print(f"3. Пересечение -X ({-R_mm:.0f} мм, 0):  {calc_exact_E(-R, 0):.4f}")
            print(f"4. Пересечение +Y (0, {R_mm:.0f} мм):   {calc_exact_E(0, R):.4f}")
            print(f"5. Пересечение -Y (0, {-R_mm:.0f} мм):  {calc_exact_E(0, -R):.4f}")

            if v_max > 0:
                img[mask] = (values / v_max * 255)
            else:
                img[mask] = 255

        img = img.astype(np.uint8)

        os.makedirs("../img", exist_ok=True)
        Image.fromarray(img).save("../img/image.png")

        plt.figure(figsize=(7, 7))
        plt.imshow(img, cmap="gray", extent=[-width / 2, width / 2, -height / 2, height / 2])
        plt.xlabel("X, м")
        plt.ylabel("Y, м")
        plt.title("Распределение освещенности")
        plt.tight_layout()
        plt.show()

        center_section = result[heightRes // 2, :]
        section_mask = mask[heightRes // 2, :]

        plot_y = np.full_like(center_section, np.nan)
        plot_y[section_mask] = center_section[section_mask]

        plt.figure(figsize=(8, 4))
        plt.plot(x, plot_y, color='blue', lw=2)
        plt.xlabel("X, м")
        plt.ylabel("Освещенность, Вт/м²")
        plt.title("Сечение распределения освещенности через центр")
        plt.grid()
        plt.tight_layout()
        plt.show()

    except ValueError as ve:
        messagebox.showerror("Ошибка ввода", str(ve))
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


root = tk.Tk()
root.title("Расчет освещенности")

params = [
    ("Ширина области W (мм)", "4000"),
    ("Высота области H (мм)", "4000"),
    ("Разрешение X (px)", "600"),
    ("Разрешение Y (px)", "600"),
    ("x источника (мм)", "10000"),
    ("y источника (мм)", "10000"),
    ("z источника (мм)", "3000"),
    ("Сила I0 (Вт/ср)", "5000"),
    ("Радиус круга (мм)", "1500")
]

entries = []

for name, value in params:
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=2, fill="x")
    label = tk.Label(frame, text=name, width=25, anchor="w")
    label.pack(side="left")
    entry = tk.Entry(frame)
    entry.insert(0, value)
    entry.pack(side="right", expand=True, fill="x")
    entries.append(entry)

(
    entry_W,
    entry_H,
    entry_Wres,
    entry_Hres,
    entry_xL,
    entry_yL,
    entry_zL,
    entry_I0,
    entry_R
) = entries

button = tk.Button(
    root,
    text="Рассчитать",
    command=calculate,
    width=20
)
button.pack(pady=10)

root.mainloop()
