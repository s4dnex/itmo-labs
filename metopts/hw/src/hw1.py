import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return 2 + x ** 2 + x ** (2 / 3) - np.log(1 + x ** (2 / 3)) - 2 * x * np.arctan(x ** (1 / 3))
def df(x):
    return 2 * x - 2 * np.arctan(x ** (1 / 3))

def cubic_approximation_step(x0, x1):
    y0, y1 = f(x0), f(x1)
    dy0, dy1 = df(x0), df(x1)
    delta = x1 - x0

    A = y0
    B = dy0 + 2 * y0 / delta
    C = y1
    D = -dy1 + 2 * y1 / delta

    alpha3 = B - D
    alpha2 = (A - B * x0 - 2 * B * x1) + (C + D * x1 + 2 * D * x0)
    alpha1 = (-2 * A + 2 * B * x0 + B * x1) * x1 + (-2 * C - 2 * D * x1 - D * x0) * x0
    alpha0 = (A - B * x0) * x1 ** 2 + (C + D * x1) * x0 ** 2

    discriminant = alpha2 ** 2 - 3 * alpha1 * alpha3
    if discriminant < 0:
        return None, None

    xm = (-alpha2 + np.sqrt(discriminant)) / (3 * alpha3)

    if not (min(x0, x1) <= xm <= max(x0, x1)):
        xm = (-alpha2 - np.sqrt(discriminant)) / (3 * alpha3)

    coeffs = (alpha3, alpha2, alpha1, alpha0, delta)
    return xm, coeffs


def plot_iteration(x0, x1, xm, coeffs, iteration):
    alpha3, alpha2, alpha1, alpha0, delta = coeffs
    x_vals = np.linspace(0.4, 1.1, 500)
    y_vals = f(x_vals)
    H_vals = (alpha3 * x_vals ** 3 + alpha2 * x_vals ** 2 + alpha1 * x_vals + alpha0) / (delta ** 2)

    plt.figure(figsize=(9, 6))
    plt.plot(x_vals, y_vals, label='f(x) Исходная функция', linewidth=2)
    plt.plot(x_vals, H_vals, '--', label='H(x) Аппроксимирующая функция', linewidth=2)
    plt.scatter([xm], [f(xm)], color='green', marker='*', s=200, zorder=6, label=f'Минимум H(x): x={xm:.6f}')
    plt.scatter([x0, x1], [f(x0), f(x1)], color='red', zorder=7, label='Узлы интерполяции')

    plt.title(f'Итерация {iteration}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.ylim(1.65, 1.9)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    a, b = 0.5, 1.0
    epsilon = 1e-7
    x0, x1 = a, b

    print(f"Поиск минимума кубической аппроксимацией на [{a}, {b}]\n")

    iteration = 1
    while True:
        xm, coeffs = cubic_approximation_step(x0, x1)
        if xm is None:
            print("Ошибка вычислений: отрицательный дискриминант.")
            break

        derivative = df(xm)

        print(f"--- Итерация {iteration} ---")
        print(f"x0 = {x0:.7f}, x1 = {x1:.7f}")
        print(f"xm = {xm:.7f}, f'(xm) = {derivative:.7f}")

        plot_iteration(x0, x1, xm, coeffs, iteration)

        if abs(derivative) <= epsilon:
            print(f"\nКритерий останова достигнут на итерации {iteration}: |f'(xm)| = {abs(derivative):.7f} <= {epsilon}")
            print(f"Ответ: x* = {xm:.7f}, f(x*) = {f(xm):.7f}")
            break

        if derivative > 0:
            x1 = xm
        else:
            x0 = xm

        iteration += 1