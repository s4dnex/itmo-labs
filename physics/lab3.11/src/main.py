import numpy as np
import matplotlib.pyplot as plt

# Входные данные
data = {
    '100 нФ':  ([1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1],
                [14.6, 17.4, 14.6, 11.2, 9.0, 7.0, 5.4, 4.2, 3.4, 3.0, 2.6]),
    '30 нФ':   ([1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7],
                [7.4, 8.4, 9.8, 12.4, 17.8, 24.0, 23.2, 20.4, 17.6, 14.6, 12.4]),
    '10 нФ':   ([3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5],
                [11.6, 14.0, 16.8, 22.8, 29.2, 30.0, 27.6, 25.6, 22.8, 19.6, 16.8]),
    '3 нФ':    ([6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9],
                [18.0, 21.2, 25.6, 33.2, 40.8, 43.6, 42.0, 40.0, 37.2, 34.0, 31.2]),
    '1 нФ':    ([11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9, 12.0, 12.1, 12.2, 12.3],
                [24.0, 27.6, 32.4, 39.8, 46.8, 50.4, 50.8, 49.6, 46.8, 44.4, 42.0]),
    '300 нФ':  ([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                [4.0, 4.32, 4.64, 5.6, 7.44, 11.6, 12.4, 8.0, 5.6, 4.0, 2.8])
}

# 1. Графики резонансных кривых
fig, axs = plt.subplots(2, 3, figsize=(14, 8))
fig.suptitle('Резонансные кривые напряжения на конденсаторе', fontsize=16)
axs = axs.flatten()

for idx, (label, (f, u)) in enumerate(data.items()):
    axs[idx].plot(f, u, 'o-', color='blue', markersize=4)
    axs[idx].set_title(f'Емкость C = {label}')
    axs[idx].set_xlabel('Частота f, кГц')
    axs[idx].set_ylabel('Напряжение $U_C$, В')
    axs[idx].grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('images/plot_resonance.png', dpi=300)

# 2. Обработка МНК
C_vals = np.array([100e-9, 30e-9, 10e-9, 3e-9, 1e-9, 300e-9])
f_res = np.array([1.2e3, 2.2e3, 4.0e3, 7.4e3, 11.9e3, 0.7e3])

x = 1 / C_vals
y = (2 * np.pi * f_res)**2

b, a = np.polyfit(x, y, 1)

plt.figure(figsize=(8, 6))
plt.plot(x, y, 'ro', label='Экспериментальные данные')
x_line = np.linspace(0, max(x)*1.05, 100)
plt.plot(x_line, a + b * x_line, 'b-', label=f'Аппроксимация МНК\n$y = {b:.2e}x {"+" if a>0 else ""} {a:.2e}$')

plt.title('Зависимость квадрата резонансной частоты от обратной емкости')
plt.xlabel('Обратная емкость $1/C$, Ф$^{-1}$')
plt.ylabel('Квадрат круговой частоты $\Omega_{res}^2$, с$^{-2}$')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('images/plot_regression.png', dpi=300)