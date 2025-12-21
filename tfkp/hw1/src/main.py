import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, ifft, fftshift, fftfreq

a = 3
t1 = 1
t2 = 33

# 1. Линейные фильтры

T_total = 100 # Большой интервал времени
dt = 0.05 # Маленький шаг дискретизации
t = np.arange(-T_total/2, T_total/2, dt) # Набор временных шагов

g = np.zeros_like(t)
g[(t >= t1) & (t <= t2)] = a # Значения функции g(t)

b, c, d = 0.5, 0.7, 5  # b - шум, c - амплитуда синуса, d - частота помехи (параметры возмущения)
xi = np.random.uniform(-1, 1, size=t.shape) # Дискретные значения шума
u = g + b*xi + c*np.sin(d*t) # Зашумленная версия g(t)

# 1.1 Фильтр первого порядка
c = 0
T_const = 3.0
num = [1]
den = [T_const, 1]
filter1 = signal.TransferFunction(num, den)

t_sim = t - t[0] # сдвигаем в [0, 100]
# Симулируем, используя t_sim, но подаем тот же сигнал u
tout, g_filtered, _ = signal.lsim(filter1, u, t_sim)

# Используем угловую частоту omega (рад/с)
W = fftshift(fftfreq(len(t), dt)) * 2 * np.pi
U_fft = fftshift(fft(u)) * dt
G_orig_fft = fftshift(fft(g)) * dt
G_filt_fft = fftshift(fft(g_filtered)) * dt

# АЧХ фильтра теоретическая: |W(iw)| = 1 / sqrt(1 + (wT)^2)
frc = 1 / np.sqrt(1 + (W * T_const)**2)

# Визуализация
plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(t, u, alpha=0.5, label='Зашумленный u(t)')
plt.plot(t, g, 'k--', label='Исходный g(t)')
plt.plot(t, g_filtered, 'r', lw=2, label=f'Отфильтрованный (T={T_const})')
plt.title('Сигнал во временной области')
plt.legend(); plt.grid()

plt.subplot(2, 1, 2)
plt.plot(W, np.abs(U_fft), alpha=0.5, label='Спектр u(t)')
plt.plot(W, np.abs(G_filt_fft), 'r', label='Спектр после фильтра')
plt.plot(W, frc * np.max(np.abs(U_fft)), 'g--', label='АЧХ (масштабированная)')
plt.xlim(-10, 10)
plt.title('Спектральный анализ (модули)')
plt.legend(); plt.grid()
plt.tight_layout(); plt.show()