import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, ifft, fftshift, fftfreq

# --- 1. Базовые настройки ---
a_param = 3
t1, t2 = 1, 33
T_total = 100
dt = 0.05
t = np.arange(-T_total / 2, T_total / 2, dt)
t_sim = t - t[0]

# Функция генерации сигнала для 1.2 (без белого шума b=0)
def generate_signals_notch(a, c_sin, d_freq):
    g = np.zeros_like(t)
    g[(t >= t1) & (t <= t2)] = a
    # Зашумленный сигнал: прямоугольник + синусоидальная помеха
    u = g + c_sin * np.sin(d_freq * t)
    return g, u

# --- 2. Функция комплексного анализа (Режекторный фильтр) ---
def analyze_notch_filtration(a, b1_const, c_sin, d_freq, omega0_const, title_suffix=""):
    g, u = generate_signals_notch(a, c_sin, d_freq)

    # --- ВРЕМЕННАЯ ФИЛЬТРАЦИЯ ---
    # Определение режекторного фильтра W2(p) = (p^2 + w0^2) / (p^2 + b1*p + w0^2)
    num = [1, 0, omega0_const**2]
    den = [1, b1_const, omega0_const**2]
    filter2 = signal.TransferFunction(num, den)

    # Пропускание сигнала u через фильтр (линейная симуляция)
    # u_filtered - отфильтрованный сигнал во временной области
    tout, u_filtered, _ = signal.lsim(filter2, u, t_sim)

    # --- ЧАСТОТНАЯ ФИЛЬТРАЦИЯ ---
    freqs = fftfreq(len(t), dt)  # Массив циклических частот (Гц)
    omegas = 2 * np.pi * freqs  # Массив угловых частот (рад/с)

    u_hat = fft(u)  # Фурье-образ зашумленного сигнала
    g_hat = fft(g)  # Фурье-образ исходного сигнала

    # Передаточная функция в частотной области: W2(iw)
    W2_iw = ( (1j * omegas)**2 + omega0_const**2 ) / ( (1j * omegas)**2 + b1_const * (1j * omegas) + omega0_const**2 )

    # АЧХ (Амплитудно-частотная характеристика) - модуль передаточной функции
    ach = np.abs(W2_iw)

    # Теоретический Фурье-образ выхода: произведение образа входа на передаточную функцию
    u_spec_hat = u_hat * W2_iw

    # Обратное преобразование Фурье - восстановление сигнала из спектра
    u_spec = np.real(ifft(u_spec_hat))

    # --- ПОДГОТОВКА ДАННЫХ ДЛЯ ГРАФИКОВ (Сдвиг спектров) ---
    omegas_shifted = fftshift(omegas)  # Центрирование частот
    g_hat_shifted = fftshift(np.abs(g_hat)) * dt
    u_hat_shifted = fftshift(np.abs(u_hat)) * dt
    u_spec_hat_shifted = fftshift(np.abs(u_spec_hat)) * dt
    u_filtered_hat_shifted = fftshift(np.abs(fft(u_filtered))) * dt
    ach_shifted = fftshift(ach)  # Центрирование АЧХ

    # --- ПОСТРОЕНИЕ ГРАФИКОВ ---
    fig, axes = plt.subplots(3, 2, figsize=(15, 15))
    fig.suptitle(f"Исследование {title_suffix}: b1={b1_const}, d={d_freq}, ω0={omega0_const}", fontsize=18)

    # 1. Временная область
    axes[0, 0].plot(t, u, color='gray', alpha=0.4, label='Зашумленный u(t)')
    axes[0, 0].plot(t, g, 'k--', lw=1.5, label='Исходный g(t)')
    axes[0, 0].plot(t, u_filtered, 'r', lw=2, label='Фильтрованный u_filt(t)')
    axes[0, 0].set_title("Сигналы во временной области")
    axes[0, 0].set_xlabel("Время t, с")
    axes[0, 0].set_ylabel("Амплитуда")
    axes[0, 0].legend(); axes[0, 0].grid(True)

    # 2. Сравнение методов
    axes[0, 1].plot(t, u_filtered, 'r', label='Фильтрованный')
    axes[0, 1].plot(t, u_spec, 'b--', label='Обратное преобр. Фурье')
    axes[0, 1].set_title("Сравнение фильтрованного и обратного преобр. Фурье")
    axes[0, 1].set_xlabel("Время t, с")
    axes[0, 1].set_ylabel("Амплитуда")
    axes[0, 1].legend(); axes[0, 1].grid(True)

    # 3. Модули спектров (Zoom в зоне частоты режекции)
    axes[1, 0].plot(omegas_shifted, u_hat_shifted, color='gray', alpha=0.4, label='|û(ω)| зашумленный')
    axes[1, 0].plot(omegas_shifted, g_hat_shifted, 'k--', label='|ĝ(ω)| исходный')
    axes[1, 0].plot(omegas_shifted, u_filtered_hat_shifted, 'r', label='|û(ω)| фильтрованный')
    axes[1, 0].set_xlim(omega0_const - 10, omega0_const + 10)
    axes[1, 0].set_title("Модули сигналов")
    axes[1, 0].set_xlabel("Угловая частота ω, рад/с"); axes[1, 0].set_ylabel("Модуль")
    axes[1, 0].legend(); axes[1, 0].grid(True)

    # 4. Сравнение спектров
    axes[1, 1].plot(omegas_shifted, u_filtered_hat_shifted, 'r', label='Фильтрованный')
    axes[1, 1].plot(omegas_shifted, u_spec_hat_shifted, 'b--', label='|W2(iω) * û(ω)|')
    axes[1, 1].set_xlim(omega0_const - 10, omega0_const + 10)
    axes[1, 1].set_title("Сравнение спектров")
    axes[1, 1].set_xlabel("Угловая частота ω, рад/с"); axes[1, 1].set_ylabel("Модуль")
    axes[1, 1].legend(); axes[1, 1].grid(True)

    # 5. АЧХ фильтра
    axes[2, 0].plot(omegas_shifted, ach_shifted, 'g', lw=2)
    axes[2, 0].set_xlim(0, omega0_const * 2)
    axes[2, 0].set_title(f"АЧХ режекторного фильтра (b1 = {b1_const})")
    axes[2, 0].set_xlabel("Угловая частота ω, рад/с")
    axes[2, 0].set_ylabel("|W2(iω)|")
    axes[2, 0].grid(True)

    axes[2, 1].axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# --- 3. Исследования ---

W0 = 5.0 # Частота, которую должен вырезать фильтр

# 3.1. Влияние b1 (ширина выреза) при идеальном попадании d = w0
for b1 in [0.2, 1.0, 5.0]:
    analyze_notch_filtration(a=3, b1_const=b1, c_sin=1.5, d_freq=W0, omega0_const=W0, title_suffix="влияния b1")

# 3.2. Влияние отклонения частоты помехи d от расчетной w0
for d_mis in [4.5, 5.0, 5.5]:
    analyze_notch_filtration(a=3, b1_const=0.5, c_sin=1.5, d_freq=d_mis, omega0_const=W0, title_suffix="влияния d")