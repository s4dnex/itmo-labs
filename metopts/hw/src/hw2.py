import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.optimize import minimize_scalar
from abc import ABC, abstractmethod

class OptimizationProblem:
    """Сущность: Задача оптимизации (содержит функцию и её градиент)"""

    def __init__(self, objective_func, gradient_func, hessian_func=None):
        self.objective = objective_func
        self.gradient = gradient_func
        self.hessian = hessian_func


class Optimizer(ABC):
    """Абстрактный класс (Интерфейс) для методов оптимизации"""

    def __init__(self, problem: OptimizationProblem, tol=0.0001, max_iter=1000):
        self.problem = problem  # Агрегация
        self.tol = tol
        self.max_iter = max_iter
        self.history = {}

    def optimize(self, initial_point):
        """Шаблонный метод оптимизации, собирающий историю приближений"""
        current_point = np.array(initial_point, dtype=float)
        self.history = {0: {'solution': current_point.copy(),
                            'objective': self.problem.objective(*current_point)}}

        for i in range(1, self.max_iter + 1):
            grad = np.array(self.problem.gradient(*current_point))

            # Критерий останова по модулю градиента
            if np.linalg.norm(grad) <= self.tol:
                break

            # Порождение нового приближения (делегируется потомкам)
            current_point = self._step(current_point, grad, i)
            self.history[i] = {'solution': current_point.copy(),
                               'objective': self.problem.objective(*current_point)}

        return current_point, self.history

    @abstractmethod
    def _step(self, point, grad, iteration):
        """Абстрактный метод, реализующий один шаг алгоритма"""
        pass


class GradientDescent(Optimizer):
    """Реализация метода градиентного спуска (с постоянным шагом)"""

    def __init__(self, problem, lr=0.01, tol=0.0001, max_iter=1000):
        super().__init__(problem, tol, max_iter)
        self.lr = lr

    def _step(self, point, grad, iteration):
        return point - self.lr * grad


class SteepestDescent(Optimizer):
    """Реализация метода наискорейшего спуска (использование одномерной оптимизации)"""

    def _step(self, point, grad, iteration):
        obj = self.problem.objective
        res = minimize_scalar(lambda alpha: obj(*(point - alpha * grad)),
                              bounds=(0, 1.5), method='bounded')
        optimal_alpha = res.x
        return point - optimal_alpha * grad


class CoordinateDescent(Optimizer):
    """Реализация метода покоординатного спуска"""

    def optimize(self, initial_point):
        current_point = np.array(initial_point, dtype=float)
        step_idx = 0
        self.history = {step_idx: {'solution': current_point.copy(),
                                   'objective': self.problem.objective(*current_point)}}

        for i in range(1, self.max_iter + 1):
            grad = np.array(self.problem.gradient(*current_point))
            if np.linalg.norm(grad) <= self.tol:
                break

            res_x = minimize_scalar(lambda alpha: self.problem.objective(current_point[0] + alpha, current_point[1]),
                                    bounds=(-1.5, 1.5), method='bounded')
            current_point[0] += res_x.x
            step_idx += 1
            self.history[step_idx] = {'solution': current_point.copy(),
                                      'objective': self.problem.objective(*current_point)}

            res_y = minimize_scalar(lambda alpha: self.problem.objective(current_point[0], current_point[1] + alpha),
                                    bounds=(-1.5, 1.5), method='bounded')
            current_point[1] += res_y.x
            step_idx += 1
            self.history[step_idx] = {'solution': current_point.copy(),
                                      'objective': self.problem.objective(*current_point)}

        return current_point, self.history

    def _step(self, point, grad, iteration):
        pass

class NewtonMethod(Optimizer):
    """Реализация метода Ньютона (дополнительно для задания 2.2)"""

    def _step(self, point, grad, iteration):
        H_inv = np.linalg.inv(self.problem.hessian(*point))
        return point - H_inv @ grad



def f(x, y):
    return x ** 3 - 12 * x ** 2 + 45 * x + y ** 3 - 2 * y ** 2 - 54
def grad_f(x, y):
    df_dx = 3 * x ** 2 - 24 * x + 45
    df_dy = 3 * y ** 2 - 4 * y
    return np.array([df_dx, df_dy])
def hessian_f(x, y):
    d2f_dx2 = 6 * x - 24
    d2f_dy2 = 6 * y - 4
    d2f_dxdy = 0
    return np.array([[d2f_dx2, d2f_dxdy], [d2f_dxdy, d2f_dy2]])

def plot_history(title: str, objective, history: dict):
    """
    Модифицированная функция: линии уровня проходят СТРОГО через вершины ломаной.
    """
    solutions_x = [v['solution'][0] for k, v in history.items()]
    solutions_y = [v['solution'][1] for k, v in history.items()]

    margin = 1.0
    x_min, x_max = min(solutions_x) - margin, max(solutions_x) + margin
    y_min, y_max = min(solutions_y) - margin, max(solutions_y) + margin

    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 400),
                         np.linspace(y_min, y_max, 400))
    target_grid_vals = objective(xx, yy)

    colorlist = ["darkblue", "blue", "aqua", "lawngreen", "gold", "darkorange", "brown"]
    newcmp = LinearSegmentedColormap.from_list("testCmap", colors=colorlist, N=256)

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    z_levels = sorted(list(set([v['objective'] for k, v in history.items()])))
    if len(z_levels) < 2:
        z_levels.append(z_levels[0] + 0.1)

    contours = ax.contour(xx, yy, target_grid_vals, levels=z_levels, cmap=newcmp, alpha=0.6)
    plt.clabel(contours, inline=1, fontsize=9, fmt="%.3f")

    plt.plot(solutions_x, solutions_y, 'o-', color='red', markersize=6, linewidth=2, label='Траектория метода')

    plt.plot(solutions_x[0], solutions_y[0], 'ks', markersize=8, label='Старт')
    plt.plot(solutions_x[-1], solutions_y[-1], 'k*', markersize=12, label='Минимум')

    plt.title(title)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    initial_point = (4.5, 1.5)
    problem = OptimizationProblem(f, grad_f, hessian_f)

    methods = {
        "Градиентный спуск (Gradient Descent)": GradientDescent(problem, lr=0.015),
        "Наискорейший спуск (Steepest Descent)": SteepestDescent(problem),
        "Покоординатный спуск (Coordinate Descent)": CoordinateDescent(problem),
        "Метод Ньютона (Newton's Method)": NewtonMethod(problem)
    }

    for name, optimizer in methods.items():
        print(f"--- Запуск: {name} ---")
        best_point, history = optimizer.optimize(initial_point)
        print(f"Найдена точка: x={best_point[0]:.6f}, y={best_point[1]:.6f}")
        print(f"Значение функции: z={f(*best_point):.6f}")
        print(f"Количество шагов в истории: {len(history) - 1}\n")

        plot_history(name, f, history)