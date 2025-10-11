import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Данные из таблицы
intervals = [(0.155, 0.169), (0.169, 0.183), (0.183, 0.197), 
             (0.197, 0.211), (0.211, 0.225), (0.225, 0.239), 
             (0.239, 0.252)]

delta_N = [6, 9, 18, 10, 6, 3, 2]
density = [8.571, 12.857, 25.714, 14.286, 8.571, 4.286, 2.857]
t_mid = [0.162, 0.176, 0.190, 0.204, 0.218, 0.232, 0.246]
rho = [5.524, 12.182, 17.741, 17.060, 10.833, 4.542, 1.326]

# Параметры гистограммы
widths = [interval[1] - interval[0] for interval in intervals]
centers = [(interval[0] + interval[1]) / 2 for interval in intervals]

# Создание фигуры
plt.figure(figsize=(12, 7))

# Построение гистограммы
bars = plt.bar(centers, density, width=widths, alpha=0.7, 
               color='lightblue', edgecolor='black', linewidth=1.2)

# Параметры функции Гаусса из формулы
mu = 0.1957
sigma = 0.02173

# Создаем плавную кривую Гаусса, используя вычисленные значения rho как ориентир
x_min, x_max = intervals[0][0], intervals[-1][1]
x_fit = np.linspace(x_min, x_max, 500)

# Вычисляем значения функции Гаусса в точках x_fit
y_fit = norm.pdf(x_fit, mu, sigma)

# Построение графика Гаусса
plt.plot(x_fit, y_fit, 'r-', linewidth=2.5)

# Добавляем подписи значений гистограммы и функции Гаусса в средних точках
for i, (center, hist_val, gauss_val) in enumerate(zip(centers, density, rho)):
    # Подпись для гистограммы (внутри столбца посередине)
    plt.text(center, hist_val / 2, f'{hist_val:.1f}', 
             ha='center', va='center', fontsize=9, color='darkblue', fontweight='bold')
    
    # Подпись для функции Гаусса (над кривой)
    plt.text(center, gauss_val + 0.8, f'{gauss_val:.1f}', 
             ha='center', va='bottom', fontsize=9, color='darkred', fontweight='bold')

# Настройка графика
plt.xlabel('t, с', fontsize=12)
plt.ylabel(f"ΔN/(N·Δt), с⁻¹\np, с⁻¹", fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)

# Подписи для интервалов
xtick_positions = [(interval[0] + interval[1]) / 2 for interval in intervals]
xtick_labels = [f'[{interval[0]:.3f}, {interval[1]:.3f}]' for interval in intervals]
plt.xticks(xtick_positions, xtick_labels, rotation=0)

# Устанавливаем пределы оси X для точного соответствия интервалу гистограммы
plt.xlim(x_min - 0.005, x_max + 0.005)

# Устанавливаем пределы оси Y, чтобы подписи помещались
y_max = max(max(density), max(rho)) + 3
plt.ylim(0, y_max)

plt.tight_layout()
plt.show()

# Вывод параметров функции Гаусса
# print(f"Параметры функции Гаусса:")
# print(f"Среднее (μ) = {mu:.4f} с")
# print(f"Стандартное отклонение (σ) = {sigma:.5f} с")
# print("\nЗначения в средних точках:")
# print("Интервал\tЦентр\tГистограмма\tГаусс (ρ)")
# for i in range(len(centers)):
#    print(f"{i+1}\t\t{centers[i]:.3f}\t{density[i]:.1f}\t\t{rho[i]:.3f}")
