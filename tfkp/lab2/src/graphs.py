import numpy as np
import matplotlib.pyplot as plt
from src.main import f_complex, compute_cn

R = 421.0
T = 1.0
N_values = [1, 2, 3, 10]


get_f = np.vectorize(f_complex)

max_N = max(N_values)
coeffs = {}
for n in range(-max_N, max_N + 1):
    coeffs[n] = compute_cn(n)

def get_GN(t_array, N, T, coeffs_dict):
    result = np.zeros_like(t_array, dtype=complex)
    for n in range(-N, N + 1):
        c_n = coeffs_dict[n]
        result += c_n * np.exp(1j * 2 * np.pi * n * t_array / T)
    return result

t_vals = np.linspace(-0.5, 1.5, 1000)
f_vals = get_f(t_vals)

fig, axes = plt.subplots(len(N_values), 2, figsize=(12, 16))
plt.subplots_adjust(hspace=0.4)

for i, N in enumerate(N_values):
    gn_vals = get_GN(t_vals, N, T, coeffs)

    # -- График Re --
    ax_re = axes[i, 0]
    # Оригинал
    ax_re.plot(t_vals, f_vals.real, 'k--', linewidth=1.5, label='Re(f(t))', alpha=0.6)
    # Аппроксимация
    ax_re.plot(t_vals, gn_vals.real, 'b-', linewidth=2, label=f'Re(G_{{{N}}}(t))')

    ax_re.set_title(f"Re: N = {N}")
    ax_re.grid(True, linestyle=':', alpha=0.7)
    ax_re.set_xlim([-0.2, 1.2])
    if i == 0: ax_re.legend(loc='upper right')

    # -- График Im --
    ax_im = axes[i, 1]
    # Оригинал
    ax_im.plot(t_vals, f_vals.imag, 'k--', linewidth=1.5, label='Im(f(t))', alpha=0.6)
    # Аппроксимация
    ax_im.plot(t_vals, gn_vals.imag, 'r-', linewidth=2, label=f'Im(G_{{{N}}}(t))')

    ax_im.set_title(f"Im: N = {N}")
    ax_im.grid(True, linestyle=':', alpha=0.7)
    ax_im.set_xlim([-0.2, 1.2])
    if i == 0: ax_im.legend(loc='upper right')

plt.show()