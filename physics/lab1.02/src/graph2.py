import matplotlib.pyplot as plt
import numpy as np

# Данные (модуль синуса)
x = np.abs(np.array([-0.008974359, -0.023076923, -0.033333333, -0.043589744, -0.053846154]))
y = np.array([0.148, 0.293, 0.485, 0.589, 0.731])

# Параметры линии тренда
B = 13.222293
A = 0.018488

# Линия тренда
x_trend = np.linspace(0.008, 0.055, 100)
y_trend = B * x_trend + A

plt.figure(figsize=(10, 6))

# Сетка
plt.grid(which='major', color='#DDDDDD', linewidth=1.0)
plt.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.8)
plt.minorticks_on()

# Линия
plt.plot(x_trend, y_trend)

# Точки
# plt.scatter(x, y, color='white')
plt.scatter(x, y, color='#5D8AA8', zorder=3)

# Убираем подписи осей, оставляем только цифры
plt.tick_params(axis='both', which='major', labelsize=16)
# Настраиваем подписи осей, чтобы ноль был только на пересечении

# Для оси X: задаем подписи, начиная не с 0
x_ticks = np.arange(0, 0.07, 0.01)
plt.xticks(x_ticks, [f'{tick:.2f}' if tick != 0 else '0' for tick in x_ticks])

# Для оси Y: задаем подписи, начиная не с 0
y_ticks = np.arange(0.1, 1.0, 0.1)
plt.yticks(y_ticks, [f'{tick:.1f}' for tick in y_ticks])

# Уравнение (можно оставить как справочную информацию)
# plt.text(0.005, 0.65, f'a = {B:.2f} · sin α + {A:.3f}', fontsize=14,
         # bbox=dict(facecolor='white', edgecolor='#B0C4DE', boxstyle='round,pad=0.5'))

# Пределы
plt.xlim(0, 0.06)
plt.ylim(0, 0.9)

plt.xlabel("sin(α)", fontsize=16)
plt.ylabel("a, м/с²", fontsize=16)

plt.tight_layout()
plt.savefig('../images/graph2.png', dpi=300)
plt.show()
