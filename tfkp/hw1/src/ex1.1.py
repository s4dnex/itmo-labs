import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, ifft, fftshift, fftfreq

# --- 1. Базовые настройки ---
a_val = 3
t1, t2 = 1, 33
T_total = 100
dt = 0.05
t = np.arange(-T_total / 2, T_total / 2, dt)
t_sim = t - t[0]  # Вектор для lsim (от 0)


# Функция генерации сигнала
def generate_signals(a, b=0.5, c=0, d=5):
    g = np.zeros_like(t)
    g[(t >= t1) & (t <= t2)] = a
    xi = np.random.uniform(-1, 1, size=t.shape)
    u = g + b * xi + c * np.sin(d * t)
    return g, u


# --- 2. Функция для комплексного анализа одного случая ---
def analyze_filtration(a, T_const, title_suffix=""):
    g, u = generate_signals(a)

    # 1. Временная фильтрация (lsim)
    filter1 = signal.TransferFunction([1], [T_const, 1])
    _, g_filt, _ = signal.lsim(filter1, u, t_sim)

    # 2. Частотная фильтрация (через FFT)
    W_freq = fftshift(fftfreq(len(t), dt)) * 2 * np.pi
    U_fft = fft(u) * dt
    W_complex = 1 / (1j * W_freq * T_const + 1)  # Передаточная функция W(iw)

    # Сдвигаем W_complex обратно, чтобы перемножить с несдвинутым U_fft
    W_complex_raw = 1 / (1j * fftfreq(len(t), dt) * 2 * np.pi * T_const + 1)
    G_fft_theory = U_fft * W_complex_raw
    g_theory = np.real(ifft(G_fft_theory) / dt)

    # --- Графики ---
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f"Исследование {title_suffix}: a={a}, T={T_const}", fontsize=16)

    # А. Временная область (Сравнение g, u, g_filt)
    axes[0, 0].plot(t, u, color='gray', alpha=0.4, label='Зашумленный u(t)')
    axes[0, 0].plot(t, g, 'k--', label='Исходный g(t)')
    axes[0, 0].plot(t, g_filt, 'r', label='Фильтрованный')
    axes[0, 0].set_title("Временная область")
    axes[0, 0].legend()
    axes[0, 0].grid()

    # Б. Сравнение lsim и FFT-метода (Задание: сравнить фильтрованный и W*u_hat)
    axes[0, 1].plot(t, g_filt, 'r', label='Фильтрованный')
    axes[0, 1].plot(t, g_theory, 'b--', label='Обратное преобр. Фурье')
    axes[0, 1].set_title("Сравнение фильтрованного и обратного преобр. Фурье")
    axes[0, 1].legend()
    axes[0, 1].grid()

    # В. Модули Фурье-образов (Zoom спектра)
    G_orig_fft = fftshift(fft(g)) * dt
    G_filt_fft = fftshift(fft(g_filt)) * dt
    axes[1, 0].plot(W_freq, np.abs(fftshift(U_fft)), color='gray', alpha=0.4, label='Зашумленный')
    axes[1, 0].plot(W_freq, np.abs(G_orig_fft), 'k--', label='Исходный')
    axes[1, 0].plot(W_freq, np.abs(G_filt_fft), 'r', label='Фильтрованный')
    axes[1, 0].set_xlim(-5, 5)  # Наиболее значимая часть спектра
    axes[1, 0].set_title("Модули сигналов")
    axes[1, 0].legend()
    axes[1, 0].grid()

    # Г. Сравнение спектров (Задание: спектр фильтрованного и W*u_hat)
    axes[1, 1].plot(W_freq, np.abs(G_filt_fft), 'r', label='Фильтрованный')
    axes[1, 1].plot(W_freq, np.abs(fftshift(G_fft_theory)), 'b--', label='|W(iw)*^u(w)|')
    axes[1, 1].set_xlim(-5, 5)
    axes[1, 1].set_title("Сравнение спектра фильтрованного сигнала и произведения спектров")
    axes[1, 1].legend()
    axes[1, 1].grid()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


# --- 3. Выполнение исследований ---

# Исследование 1: Фиксируем a, меняем T
for T in [0.2, 3.0, 10.0]:
    analyze_filtration(a=3, T_const=T, title_suffix="влияния T")

# Исследование 2: Фиксируем T, меняем a
for a in [0.6, 3.0, 10.0]:
    analyze_filtration(a=a, T_const=3.0, title_suffix="влияние a")

# --- 4. Отдельный график АЧХ (для финального отчета) ---
W_plot = np.linspace(-10, 10, 1000)
T_fixed = 3.0
ach = 1 / np.sqrt(1 + (W_plot * T_fixed) ** 2)
plt.figure(figsize=(8, 4))
plt.plot(W_plot, ach, label=f'T = {T_fixed}')
plt.title(f"АЧХ фильтра 1-го порядка (T={T_fixed})")
plt.xlabel("Частота ω, рад/с")
plt.ylabel("|W(iω)|")
plt.grid();
plt.legend()
plt.show()