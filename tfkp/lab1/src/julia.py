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
    --no-axes - Сохранить только изображение множества

Примеры:
    python julia.py --c -0.5251993+0.5251993i --width 1200 --height 800 --max-iter 400
    python julia.py --c -0.4+0.6j --xmin -1.5 --xmax 1.5 --ymin -1.5 --ymax 1.5
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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
    Можно взять более строгую оценку R из R^2 - R > |c| => R = (1 + sqrt(1 + 4|c|)) / 2
    """
    ac = abs(c)
    r = 2.0
    try:
        r_candidate = (1.0 + math.sqrt(1.0 + 4.0 * ac)) / 2.0
        if r_candidate > r:
            r = r_candidate
    except Exception:
        pass
    return r


def julia_set(c: complex, xmin: float, xmax: float, ymin: float, ymax: float,
              width: int, height: int, max_iter: int):
    """
    Возвращает массив с "итерационной глубиной" (escape time) и маску не сбежавших точек.
    Для более красивой раскраски возвращаем вещественное значение с плавной нормировкой.
    """
    # Создаем сетку комплексной плоскости
    xs = np.linspace(xmin, xmax, width)
    ys = np.linspace(ymin, ymax, height)
    x, y = np.meshgrid(xs, ys)
    z = x + 1j * y

    # Итерации
    c_iters = np.full_like(z, fill_value=c, dtype=np.complex128)
    # Итерационные значения
    z = z.copy()
    # Массив для записи номера итерации, когда точка убежала
    it_count = np.full(z.shape, fill_value=max_iter, dtype=float)  # float для smooth
    # Булевы маски: еще не убежали
    not_escaped = np.ones(z.shape, dtype=bool)

    r = escape_radius(c)

    for n in range(max_iter):
        # на текущих позициях выполняем одну итерацию
        z[not_escaped] = z[not_escaped] * z[not_escaped] + c_iters[not_escaped]
        # вычисляем, какие из них убегают сейчас
        escaped_now = np.abs(z) > r
        # фиксируем итерацию (сглаживание ниже)
        newly_escaped = escaped_now & not_escaped
        if np.any(newly_escaped):
            # smooth iteration count: n + 1 - log(log|z|)/log 2
            zn = z[newly_escaped]
            # предохранение от log(0)
            with np.errstate(all='ignore'):
                smooth = n + 1 - np.log(np.log(np.abs(zn))) / np.log(2.0)
            # где log лог дал NaN/inf — заменим на n+1
            smooth = np.where(np.isfinite(smooth), smooth, n + 1.0)
            it_count[newly_escaped] = smooth
        not_escaped &= ~escaped_now
        # Если все убежали — можно остановить цикл
        if not np.any(not_escaped):
            break

    # Точки, не убежавшие — считаем принадлежащими заполненному множеству
    inside_mask = it_count >= max_iter
    return it_count, inside_mask


def plot_julia(counts, inside_mask, xmin, xmax, ymin, ymax, cmap, title=None):
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


def plot_julia_no_axes(counts, inside_mask, xmin, xmax, ymin, ymax, cmap, title=None, dpi=300):
    """
    Сохраняет изображение без осей и полей. Использует глобальные args.width/height,
    чтобы получить точный размер в пикселях при сохранении.
    """
    # нормализация: исключаем точки, которые не убежали, чтобы корректно вычислить vmin/vmax
    escaped_mask = ~inside_mask
    if np.any(escaped_mask):
        vmin = np.min(counts[escaped_mask])
        vmax = np.max(counts[escaped_mask])
    else:
        vmin, vmax = np.min(counts), np.max(counts)

    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    cmap_obj = plt.get_cmap(cmap)

    # преобразуем в RGBA и затем заменим точки внутри множества на чёрный
    rgba = cmap_obj(norm(counts))
    rgba[inside_mask] = (0.0, 0.0, 0.0, 1.0)  # чёрный, полностью непрозрачный

    # задаём размер фигуры так, чтобы сохранить ровно args.width x args.height пикселей
    try:
        width_px = int(args.width)
        height_px = int(args.height)
    except Exception:
        width_px, height_px = 800, 600
    figsize = (width_px / dpi, height_px / dpi)

    fig = plt.figure(figsize=figsize, dpi=dpi)
    # создаём ось, занимающую всю фигуру, без рамки
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0), frameon=False)
    ax.set_axis_off()

    extent = (xmin, xmax, ymin, ymax)
    ax.imshow(rgba, origin='lower', extent=extent, interpolation='bilinear', aspect='auto')

    # формируем безопасное имя файла (чтобы плюс/минус/j не ломали имя)
    c_str = str(args.c)
    img_name = f"img/julia_{c_str}_{args.max_iter}_no_axes.png"

    # Сохранение: bbox_inches='tight' + pad_inches=0 убирают поля; transparent можно ставить True
    fig.savefig(img_name, dpi=dpi, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    print(f"Изображение множества (без осей) сохранено: {img_name}")


def run_cli():
    parser = argparse.ArgumentParser(description="Множество Жюлиа f(z)=z^2 + c")
    parser.add_argument('--c', type=parse_complex, required=True, help="Константа c, например -0.5251993+0.5251993i")
    parser.add_argument('--width', type=int, default=800, help="Ширина изображения в пикселях")
    parser.add_argument('--height', type=int, default=600, help="Высота изображения в пикселях")
    parser.add_argument('--xmin', type=float, default=-1.5, help="Мин. z (вещественная часть)")
    parser.add_argument('--xmax', type=float, default=1.5, help="Макс. z (вещественная часть)")
    parser.add_argument('--ymin', type=float, default=-1.2, help="Мин. z (мнимая часть)")
    parser.add_argument('--ymax', type=float, default=1.2, help="Макс. z (мнимая часть)")
    parser.add_argument('--max-iter', type=int, default=300, help="Макс. кол-во итераций")
    parser.add_argument('--cmap', type=str, default='nipy_spectral', help="Цветовая палитра (colormap из matplotlib)")
    parser.add_argument('--no-axes', action="store_true", help="Сохранить только изображение множества")
    global args
    args = parser.parse_args()

    print(f"Построение множества Жюлиа для c = {args.c} с макс. кол-вом итераций n = {args.max_iter}")
    counts, inside = julia_set(args.c, args.xmin, args.xmax, args.ymin, args.ymax,
                               args.width, args.height, args.max_iter)

    title = f"Множество Жюлиа f(z)=z^2 + {args.c} (n={args.max_iter})"
    if args.no_axes:
        plot_julia_no_axes(counts, inside, args.xmin, args.xmax, args.ymin, args.ymax, cmap=args.cmap, title=title)
    else:
        plot_julia(counts, inside, args.xmin, args.xmax, args.ymin, args.ymax, cmap=args.cmap, title=title)

    return


if __name__ == '__main__':
    run_cli()
