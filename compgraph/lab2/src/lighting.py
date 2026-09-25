import math


class Vector:
    """Трехмерный вектор с координатами x, y, z."""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: "Vector") -> "Vector":
        """Сумма векторов."""
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        """Разность векторов."""
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, k: float) -> "Vector":
        """Умножение вектора на число."""
        return Vector(self.x * k, self.y * k, self.z * k)

    def dot(self, other: "Vector") -> float:
        """Скалярное произведение векторов."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def length(self) -> float:
        """Длина вектора."""
        return math.sqrt(self.dot(self))

    def normalize(self) -> "Vector":
        """Единичный вектор того же направления."""
        return self * (1.0 / self.length())


class LightSource:
    def __init__(self, x: float, y: float, z: float, intensity: float):
        self.position = Vector(x, y, z)  # мм
        self.intensity = intensity  # I0, Вт/ср, сила излучения вдоль оси (theta = 0)


def calculate_luminance(point: Vector,
                        normal: Vector,
                        viewer: Vector,
                        lights: list[LightSource],
                        diffuse_coef: float,
                        specular_coef: float,
                        shininess: float) -> float:
    """
    point         - точка на сфере, мм
    normal        - единичная нормаль к сфере в этой точке
    viewer        - координаты наблюдателя, мм
    lights        - список источников света
    diffuse_coef  - kd, коэффициент диффузного отражения
    specular_coef - ks, коэффициент зеркального отражения
    shininess     - ke, показатель блеска
    Возвращает яркость L в точке, Вт/(м^2*ср).
    """
    luminance = 0.0

    # единичный вектор от точки к наблюдателю (v)
    to_viewer = (viewer - point).normalize()

    # ось диаграммы излучения источника направлена вниз, против оси Z
    light_axis = Vector(0.0, 0.0, -1.0)

    for light in lights:
        # s - вектор от источника к точке: s = P - P_L
        light_to_point = point - light.position
        distance = light_to_point.length()  # мм

        # сила излучения в направлении точки: I = I0 * cos(theta)
        cos_theta = light_to_point.dot(light_axis) / distance
        if cos_theta <= 0:
            continue  # назад источник не светит
        intensity = light.intensity * cos_theta

        # единичный вектор от точки к источнику
        to_light = (light.position - point).normalize()

        # угол между нормалью и направлением на источник
        cos_sigma = to_light.dot(normal)
        if cos_sigma <= 0:
            continue  # точка на обратной стороне сферы относительно источника

        # освещенность E = I * cos(sigma) / R^2
        distance_m = distance / 1000.0  # мм в м
        illuminance = intensity * cos_sigma / distance_m ** 2

        # биссектриса между наблюдателем и источником
        halfway = (to_viewer + to_light).normalize()
        cos_halfway = max(halfway.dot(normal), 0.0)

        # f = kd + ks * (h * N)^ke
        reflection = diffuse_coef + specular_coef * cos_halfway ** shininess

        luminance += illuminance * reflection

    return luminance / math.pi


def find_intersection(viewer: Vector,
                      direction: Vector,
                      center: Vector,
                      radius: float) -> Vector | None:
    """
    Первая точка пересечения луча P(t) = viewer + t * direction со сферой.
    Возвращает None, если луч не пересекает сферу.
    """
    # Ray(t) = viewer + t * direction
    # direction = viewer - pixel_center

    center_to_viewer = viewer - center

    # подставляем луч в уравнение сферы |P - C|^2 = R^2 -> a*t^2 + b*t + c = 0
    coef_a = direction.dot(direction)
    coef_b = 2.0 * direction.dot(center_to_viewer)
    coef_c = center_to_viewer.dot(center_to_viewer) - radius ** 2
    discriminant = coef_b ** 2 - 4 * coef_a * coef_c
    if discriminant < 0:
        return None

    # ближайший корень - первая точка пересечения со сферой
    t = (-coef_b - math.sqrt(discriminant)) / (2 * coef_a)
    if t <= 0:
        return None  # сфера позади наблюдателя

    return viewer + direction * t


def render(width: float,
           height: float,
           width_resolution: int,
           viewer: Vector,
           center: Vector,
           radius: float,
           lights: list[LightSource],
           diffuse_coef: float,
           specular_coef: float,
           shininess: float) -> tuple[list[list[float]], list[list[Vector | None]], float]:
    """
    Экран лежит в плоскости z = 0, его центр в начале координат.
    Через центр каждого пикселя из точки наблюдателя проводится луч,
    ищется его первое пересечение со сферой и в этой точке считается яркость.

    Возвращает:
      luminance     - яркость каждого пикселя (0 там, где сферы нет),
      sphere_points - точка сферы для каждого пикселя (None там, где сферы нет),
      height_real   - реальная высота экрана, кратная размеру пикселя.
    """
    pixel_size = width / width_resolution
    height_resolution = int(round(height / pixel_size))
    height_real = height_resolution * pixel_size

    luminance: list[list[float]] = []
    sphere_points: list[list[Vector | None]] = []

    for row in range(height_resolution):
        luminance_row: list[float] = []
        points_row: list[Vector | None] = []

        for col in range(width_resolution):
            # центр пикселя на экране (строка 0 - верх изображения)
            pixel_x = -width / 2 + (col + 0.5) * pixel_size
            pixel_y = height_real / 2 - (row + 0.5) * pixel_size
            pixel = Vector(pixel_x, pixel_y, 0.0)

            direction = pixel - viewer
            point = find_intersection(viewer, direction, center, radius)

            if point is None:
                luminance_row.append(0.0)
                points_row.append(None)
            else:
                normal = (point - center).normalize()
                value = calculate_luminance(point, normal, viewer, lights,
                                            diffuse_coef, specular_coef, shininess)
                luminance_row.append(value)
                points_row.append(point)

        luminance.append(luminance_row)
        sphere_points.append(points_row)

    return luminance, sphere_points, height_real


def to_image(luminance: list[list[float]], max_luminance: float) -> list[list[int]]:
    """Нормировка яркости на максимальное значение в диапазон 0-255."""
    image: list[list[int]] = []
    for luminance_row in luminance:
        image_row: list[int] = []
        for value in luminance_row:
            if max_luminance > 0:
                image_row.append(round(value / max_luminance * 255))
            else:
                image_row.append(0)
        image.append(image_row)
    return image
