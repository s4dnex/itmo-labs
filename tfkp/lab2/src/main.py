import numpy as np
from scipy.integrate import quad

R = 421.0
T = 1.0

def f_complex(t):
    val = 0j
    t_shifted = (t + T / 8) % T - T / 8

    if -T / 8 <= t_shifted < T / 8:
        val = R + 1j * (8 * R * t_shifted / T)
    elif T / 8 <= t_shifted < 3 * T / 8:
        val = (2 * R - 8 * R * t_shifted / T) + 1j * R
    elif 3 * T / 8 <= t_shifted < 5 * T / 8:
        val = -R + 1j * (4 * R - 8 * R * t_shifted / T)
    elif 5 * T / 8 <= t_shifted < 7 * T / 8:
        val = (-6 * R + 8 * R * t_shifted / T) - 1j * R
    else:
        if t_shifted > 0:
            val = (-6 * R + 8 * R * t_shifted / T) - 1j * R
        else:
            val = R + 1j * (8 * R * t_shifted / T)

    return val


def compute_cn(n):
    omega = 2 * np.pi * n / T

    # f(t) * e^(-i * omega * t) = (Re_f + i*Im_f) * (cos(wt) - i*sin(wt))
    def integrand_real(t):
        val = f_complex(t)
        # Re = Re_f * cos - Im_f * sin
        return val.real * np.cos(omega * t) + val.imag * np.sin(omega * t)
    def integrand_imag(t):
        val = f_complex(t)
        # Im = Im_f * cos + Re_f * (-sin)
        return val.imag * np.cos(omega * t) - val.real * np.sin(omega * t)


    points = [-T / 8, T / 8, 3 * T / 8, 5 * T / 8, 7 * T / 8]

    res_real, _ = quad(integrand_real, -T / 8, 7 * T / 8, points=points)
    res_imag, _ = quad(integrand_imag, -T / 8, 7 * T / 8, points=points)

    return (res_real + 1j * res_imag) / T


if __name__ == "__main__":
    N = int(input("N: "))
    print(f"Результаты расчета через SciPy (R={R}, T={T}):")
    print(f"{'n':<3} | {'Re(cn)':<10} | {'Im(cn)':<10} | {'Abs(cn)':<10}")
    print("-" * 45)

    for n in range(-N, N + 1):
        c = compute_cn(n)

        re_val = c.real  # 0.0 if abs(c.real) < 1e-10 else c.real
        im_val = c.imag  # 0.0 if abs(c.imag) < 1e-10 else c.imag

        print(f"{n:<3} | {re_val:<10.4f} | {im_val:<10.4f} | {abs(c):<10.4f}")
        # print(*[n, re_val, im_val, abs(c)], sep="\t")