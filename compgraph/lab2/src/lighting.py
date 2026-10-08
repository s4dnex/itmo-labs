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

    def cross(self, other: "Vector") -> "Vector":
        """Векторное произведение векторов."""
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def length(self) -> float:
        """Длина вектора."""
        return math.sqrt(self.dot(self))

    def normalize(self) -> "Vector":
        """Единичный вектор того же направления."""
        return self * (1.0 / self.length())


class LightSource:
    def __init__(self, x: float, y: float, z: float, intensity: float,
                 direction: Vector = Vector(0.0, 0.0, -1.0)):
        self.position = Vector(x, y, z)  # позиция источника, мм
        self.intensity = intensity  # сила излучения вдоль оси, Вт/ср
        self.direction = direction.normalize()  # единичный вектор направления освещения


class Camera:
    """
    Наблюдатель с экраном. Экран - прямоугольник, перпендикулярный направлению взгляда,
    его центр лежит на оси взгляда на расстоянии screen_distance от наблюдателя.

    yaw   - поворот по горизонтали: угол поворота вокруг оси Z от оси +Y по часовой стрелке (к оси +X), градусы
    pitch - наклон по вертикали: угол от горизонтальной плоскости (-90 - вниз по оси Z, 90 - вверх), градусы
    """

    def __init__(self, position: Vector, yaw: float, pitch: float, screen_distance: float):
        self.position = position
        self.yaw = yaw
        self.pitch = pitch
        self.screen_distance = screen_distance  # мм

        yaw_rad = math.radians(yaw)
        pitch_rad = math.radians(pitch)
        # направление взгляда
        self.forward = Vector(math.cos(pitch_rad) * math.sin(yaw_rad),
                              math.cos(pitch_rad) * math.cos(yaw_rad),
                              math.sin(pitch_rad))
        self.right = Vector(math.cos(yaw_rad), -math.sin(yaw_rad), 0.0)
        self.up = self.right.cross(self.forward)

    def screen_point(self, u: float, v: float) -> Vector:
        return (self.position + self.forward * self.screen_distance
                + self.right * u + self.up * v)


def look_at_angles(viewer: Vector, target: Vector) -> tuple[float, float]:
    """Углы (yaw, pitch) в градусах, при которых наблюдатель смотрит на точку target."""
    direction = target - viewer
    horizontal = math.hypot(direction.x, direction.y)
    yaw = math.degrees(math.atan2(direction.x, direction.y))
    pitch = math.degrees(math.atan2(direction.z, horizontal))
    return yaw, pitch


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

    # единичный вектор от точки к наблюдателю
    to_viewer = (viewer - point).normalize()

    for light in lights:
        # s - вектор от источника к точке: s = P - P_L
        light_to_point = point - light.position
        distance = light_to_point.length()  # мм

        # сила излучения в направлении точки: I = I0 * cos(theta)
        cos_theta = light_to_point.dot(light.direction) / distance
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
           camera: Camera,
           center: Vector,
           radius: float,
           lights: list[LightSource],
           diffuse_coef: float,
           specular_coef: float,
           shininess: float) -> tuple[list[list[float]], list[list[Vector | None]], float]:
    """
    Экран перпендикулярен направлению взгляда камеры, его центр лежит на оси взгляда.
    Через центр каждого пикселя из точки наблюдателя проводится луч,
    ищется его первое пересечение со сферой и в этой точке считается яркость.

    Возвращает:
      luminance     - яркость каждого пикселя (0 там, где сферы нет),
      sphere_points - точка сферы для каждого пикселя (None там, где сферы нет),
      height_real   - реальная высота экрана, кратная размеру пикселя.
    """
    viewer = camera.position
    pixel_size = width / width_resolution
    height_resolution = int(round(height / pixel_size))
    height_real = height_resolution * pixel_size

    luminance: list[list[float]] = []
    sphere_points: list[list[Vector | None]] = []

    for row in range(height_resolution):
        luminance_row: list[float] = []
        points_row: list[Vector | None] = []

        for col in range(width_resolution):
            # центр пикселя в экранных координатах
            pixel_u = -width / 2 + (col + 0.5) * pixel_size
            pixel_v = height_real / 2 - (row + 0.5) * pixel_size
            pixel = camera.screen_point(pixel_u, pixel_v)

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
    """Нормировка яркости на максимальное значение в диапазон от 0 до 255."""
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
