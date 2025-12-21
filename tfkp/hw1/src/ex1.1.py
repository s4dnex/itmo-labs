import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, ifft, fftshift, fftfreq

# --- 1. Базовые настройки ---
a_param = 3  # Амплитуда полезного сигнала
t1, t2 = 1, 33  # Временной интервал импульса
T_total = 100  # Общая длительность времени
dt = 0.05  # Шаг дискретизации
t = np.arange(-T_total / 2, T_total / 2, dt)  # Вектор времени
t_sim = t - t[0]  # Вектор времени для lsim (начинается с 0)

# Функция генерации сигнала
def generate_signals(a, b_noise=0.5, c_sin=0, d_freq=5):
    g = np.zeros_like(t)
    g[(t >= t1) & (t <= t2)] = a  # Исходный прямоугольный сигнал
    xi = np.random.uniform(-1, 1, size=t.shape)  # Белый шум
    # Зашумленный сигнал: сигнал + шум + синусоидальная помеха
    u = g + b_noise * xi + c_sin * np.sin(d_freq * t)
    return g, u


# --- 2. Функция комплексного анализа ---
def analyze_filtration(a, T_const, title_suffix=""):
    g, u = generate_signals(a)

    # --- ВРЕМЕННАЯ ФИЛЬТРАЦИЯ ---
    # Определение фильтра 1-го порядка W(p) = 1 / (T*p + 1)
    num = [1]
    den = [T_const, 1]
    filter1 = signal.TransferFunction(num, den)

    # Пропускание сигнала u через фильтр (линейная симуляция)
    # u_filtered - отфильтрованный сигнал во временной области
    tout, u_filtered, _ = signal.lsim(filter1, u, t_sim)

    # --- ЧАСТОТНАЯ ФИЛЬТРАЦИЯ ---
    freqs = fftfreq(len(t), dt)  # Массив циклических частот (Гц)
    omegas = 2 * np.pi * freqs  # Массив угловых частот (рад/с)

    u_hat = fft(u)  # Фурье-образ зашумленного сигнала
    g_hat = fft(g)  # Фурье-образ исходного сигнала

    # Передаточная функция в частотной области: W(iw) = 1 / (T * i * w + 1)
    W_iw = 1 / (T_const * 1j * omegas + 1)

    # АЧХ (Амплитудно-частотная характеристика) - модуль передаточной функции
    ach = np.abs(W_iw)

    # Теоретический Фурье-образ выхода: произведение образа входа на передаточную функцию
    u_spec_hat = u_hat * W_iw

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
    fig.suptitle(f"Исследование {title_suffix}: a={a}, T={T_const}", fontsize=18)

    # 1. Временная область: исходный, зашумленный, фильтрованный
    axes[0, 0].plot(t, u, color='gray', alpha=0.4, label='Зашумленный u(t)')
    axes[0, 0].plot(t, g, 'k--', lw=1.5, label='Исходный g(t)')
    axes[0, 0].plot(t, u_filtered, 'r', lw=2, label='Фильтрованный u(t)')
    axes[0, 0].set_title("Сигналы во временной области")
    axes[0, 0].set_xlabel("Время t, с");
    axes[0, 0].set_ylabel("Амплитуда")
    axes[0, 0].legend();
    axes[0, 0].grid(True)

    # 2. Сравнение методов: lsim vs Обратное БПФ
    axes[0, 1].plot(t, u_filtered, 'r', label='Фильтрованный')
    axes[0, 1].plot(t, u_spec, 'b--', label='Обратное преобр. Фурье')
    axes[0, 1].set_title("Сравнение фильтрованного и обратного преобр. Фурье")
    axes[0, 1].set_xlabel("Время t, с");
    axes[0, 1].set_ylabel("Амплитуда")
    axes[0, 1].legend();
    axes[0, 1].grid(True)

    # 3. Модули спектров (Сравнение образов)
    axes[1, 0].plot(omegas_shifted, u_hat_shifted, color='gray', alpha=0.4, label='|û(ω)| зашумленный')
    axes[1, 0].plot(omegas_shifted, g_hat_shifted, 'k--', label='|ĝ(ω)| исходный')
    axes[1, 0].plot(omegas_shifted, u_filtered_hat_shifted, 'r', label='|û(ω)| фильтрованный')
    axes[1, 0].set_xlim(-10, 10);
    axes[1, 0].set_title("Модули сигналов")
    axes[1, 0].set_xlabel("Угловая частота ω, рад/с");
    axes[1, 0].set_ylabel("Модуль")
    axes[1, 0].legend();
    axes[1, 0].grid(True)

    # 4. Сравнение спектров фильтрованного сигнала и произведения W*u_hat
    axes[1, 1].plot(omegas_shifted, u_filtered_hat_shifted, 'r', label='Фильтрованный')
    axes[1, 1].plot(omegas_shifted, u_spec_hat_shifted, 'b--', label='|W(iω) * û(ω)|')
    axes[1, 1].set_xlim(-10, 10);
    axes[1, 1].set_title("Сравнение спектров")
    axes[1, 1].set_xlabel("Угловая частота ω, рад/с");
    axes[1, 1].set_ylabel("Модуль")
    axes[1, 1].legend();
    axes[1, 1].grid(True)

    # 5. АЧХ фильтра
    axes[2, 0].plot(omegas_shifted, ach_shifted, 'g', lw=2)
    axes[2, 0].set_xlim(-20, 20);
    axes[2, 0].set_title(f"АЧХ фильтра (T = {T_const})")
    axes[2, 0].set_xlabel("Угловая частота ω, рад/с");
    axes[2, 0].set_ylabel("|W(iω)|")
    axes[2, 0].grid(True)

    # 6. Пустой или дополнительный (удаляем или используем)
    axes[2, 1].axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


# --- 3. Выполнение исследований ---

# Исследование влияния T (при постоянном a)
# Здесь для каждого T будет свой набор графиков и своя АЧХ
for T in [0.5, 2.0, 10.0]:
    analyze_filtration(a=3, T_const=T, title_suffix="влияния T")

# Исследование влияния a (при постоянном T)
for a in [0.5, 3.0, 10.0]:
    analyze_filtration(a=a, T_const=2.0, title_suffix="влияния a")