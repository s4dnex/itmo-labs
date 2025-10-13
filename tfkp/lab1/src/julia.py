"""
julia.py — строит заполненное множество Жюлиа для f(z) = z^2 + c

Требования:
    numpy, matplotlib

Параметры:
    --c - константа c, например -0.5251993+0.5251993i
    --width - ширина изображения в пикселях
    --height - Высота изображения в пикселях
    --xmin - мин. z (вещественная часть)
    --xmax - макс. z (вещественная часть)
    --ymin - мин. z (мнимая часть)
    --ymax - макс. z (мнимая часть)
    --max-iter - макс. кол-во итераций
    --cmap - цветовая палитра (colormap из matplotlib)

Примеры:
    python julia.py --c -0.5251993+0.5251993i --width 1200 --height 800 --max-iter 400
    python julia.py --c -0.4+0.6j --xmin -1.5 --xmax 1.5 --ymin -1.5 --ymax 1.5
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
import math

global args


def parse_complex(s: str) -> complex:
    """Парсер комплексной строки: принимает формы 'a+bi', 'a+bj', '-0.5+0.6j' и т.п."""
    s = s.strip().replace(' ', '').replace('i', 'j')
    try:
        return complex(s)
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Не удалось получить комплексное число из '{s}': {e}")


def escape_radius(c: complex) -> float:
    """
    Для полинома z^2 + c достаточен радиус 2 для проверки убегания.
    Можно взять более строгую оценку R из R^2 - R > |c| => R = (1 + sqrt(4|c|)) / 2
    """
    ac = abs(c)
    r = 2.0
    try:
        r_candidate = (1.0 + math.sqrt(4.0 * ac)) / 2.0
        if r_candidate > r:
            r = r_candidate
    except Exception:
        pass
    return r


def julia_set(c: complex, xmin: float, xmax: float, ymin: float, ymax: float,
              width: int, height: int, max_iter: int):
    """
    Возвращает массив с моментом "убегания".
    """
    # Создаем сетку комплексной плоскости
    xs = np.linspace(xmin, xmax, width)
    ys = np.linspace(ymin, ymax, height)
    x, y = np.meshgrid(xs, ys)
    z = x + 1j * y

    # Итерации
    c_iters = np.full_like(z, fill_value=c, dtype=np.complex128)
    # Массив для записи номера итерации, когда точка убежала
    iter_count = np.full(z.shape, fill_value=max_iter, dtype=float)  # float для smooth
    # Булевы маски: еще не убежали
    not_escaped = np.ones(z.shape, dtype=bool)

    r = escape_radius(c)

    for n in range(max_iter):
        # на текущих позициях выполняем одну итерацию
        z[not_escaped] = z[not_escaped] * z[not_escaped] + c_iters[not_escaped]

        escaped_now = np.abs(z) > r
        newly_escaped = escaped_now & not_escaped
        if np.any(newly_escaped):
            iter_count[newly_escaped] = n + 1
        not_escaped &= ~escaped_now

        # Если все убежали — можно остановить цикл
        if not np.any(not_escaped):
            break

    # Точки, не убежавшие — считаем принадлежащими заполненному множеству
    return iter_count


def plot_julia(counts, xmin, xmax, ymin, ymax, cmap, title=None):
    extent = (xmin, xmax, ymin, ymax)
    fig, ax = plt.subplots(figsize=(8, 6))
    # Отображаем: для точек, входящих в множество, ставим чёрный цвет (или другой фон)
    # Для убегающих используем градиент по counts
    img = ax.imshow(counts, origin='lower', extent=extent, cmap=cmap, interpolation='bilinear')
    # Наложим контур (чёрные) для внутри-маски, если нужно: заменим пиксели внутри на 0 (чёрный)
    # Для читаемости оставим как есть — внутри точки имеют большие значения (max_iter)
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')
    if title:
        ax.set_title(title)
    plt.colorbar(img, ax=ax, label='Момент "убегания"')
    plt.tight_layout()

    img_name = f"img/julia_{args.c}_{args.max_iter}.png"
    plt.savefig(img_name, dpi=300)
    print(f"Изображение множества сохранено: {img_name}")
    plt.show()


def run_cli():
    parser = argparse.ArgumentParser(description="Множество Жюлиа f(z)=z^2 + c")
    parser.add_argument('--c', type=parse_complex, required=True, help="Константа c, например -0.5251993+0.5251993i")
    parser.add_argument('--width', type=int, default=2048, help="Ширина изображения в пикселях")
    parser.add_argument('--height', type=int, default=2048, help="Высота изображения в пикселях")
    parser.add_argument('--xmin', type=float, default=-1.75, help="Мин. z (вещественная часть)")
    parser.add_argument('--xmax', type=float, default=1.75, help="Макс. z (вещественная часть)")
    parser.add_argument('--ymin', type=float, default=-1.5, help="Мин. z (мнимая часть)")
    parser.add_argument('--ymax', type=float, default=1.5, help="Макс. z (мнимая часть)")
    parser.add_argument('--max-iter', type=int, default=500, help="Макс. кол-во итераций")
    parser.add_argument('--cmap', type=str, default='nipy_spectral', help="Цветовая палитра (colormap из matplotlib)")
    global args
    args = parser.parse_args()

    print(f"Построение множества Жюлиа для c = {args.c} с макс. кол-вом итераций n = {args.max_iter}")
    counts = julia_set(args.c, args.xmin, args.xmax, args.ymin, args.ymax,
                       args.width, args.height, args.max_iter)

    title = f"Множество Жюлиа f(z)=z^2 + {args.c} (n={args.max_iter})"
    plot_julia(counts, args.xmin, args.xmax, args.ymin, args.ymax, cmap=args.cmap, title=title)

    return


if __name__ == '__main__':
    run_cli()
