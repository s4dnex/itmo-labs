import torch
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.optim.optimizer import Optimizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns


# ==========================================
# Задание 1: Функция и Анализ
# ==========================================

class CustomGD(Optimizer):
    """
    Собственная реализация классического чистого градиентного спуска (Vanilla Gradient Descent).
    Никаких моментов, никаких адаптивных шагов — строго шаг в сторону антиградиента.
    """

    def __init__(self, params, lr=1e-3):
        defaults = dict(lr=lr)
        super(CustomGD, self).__init__(params, defaults)

    def step(self, closure=None):
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue

                # Получаем текущий градиент
                d_p = p.grad.data

                # Обновляем веса: w_new = w_old - lr * grad
                p.data.add_(d_p, alpha=-group['lr'])

        return loss

def f_val(x, y):
    return 10 ** (-2) * (8 * x ** 2 + 2 * x * y - x - 2 * y - 7)


def objective(pt):
    x, y = pt[0], pt[1]
    return 10 ** (-2) * (8 * x ** 2 + 2 * x * y - x - 2 * y - 7)


def plot_function_contours():
    """Строит компактный и красочный график линий уровня для Задания 1"""
    X = np.linspace(-20, 20, 800)
    Y = np.linspace(-50, 50, 800)
    X, Y = np.meshgrid(X, Y)
    Z = f_val(X, Y)

    plt.figure(figsize=(7, 5))
    # Делаем 40 уровней, чтобы линии были цветными и различимыми
    levels = np.linspace(np.min(Z), np.max(Z), 50)
    cp = plt.contour(X, Y, Z, levels=levels, cmap='rainbow', alpha=0.7)
    # Добавляем инлайн-подписи значений на линиях уровня
    plt.clabel(cp, inline=True, fontsize=8, fmt='%.1f')

    # Отмечаем ключевые точки
    plt.plot(1, -7.5, 'g*', markersize=10, label='Седловая точка (1, -7.5)')
    plt.plot(-99 / 16, 50, 'b*', markersize=10, label='Глобальный минимум (-6.19, 50)')

    # plt.title("Линии уровня функции f(x, y)")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim([-20, 20])
    plt.ylim([-50, 50])
    plt.legend(loc='lower right', framealpha=0.9)

    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()  # Делает график компактным (убирает белые рамки)
    plt.show()


# ==========================================
# Задание 2: Кастомный AdamW
# ==========================================

class CustomAdamW(Optimizer):
    def __init__(self, params, lr=1e-3, betas=(0.9, 0.999), eps=1e-8, weight_decay=1e-2):
        defaults = dict(lr=lr, betas=betas, eps=eps, weight_decay=weight_decay)
        super(CustomAdamW, self).__init__(params, defaults)

    def step(self, closure=None):
        loss = None
        if closure is not None: loss = closure()

        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None: continue
                grad = p.grad.data
                state = self.state[p]

                if len(state) == 0:
                    state['step'] = 0
                    state['exp_avg'] = torch.zeros_like(p.data)
                    state['exp_avg_sq'] = torch.zeros_like(p.data)

                exp_avg, exp_avg_sq = state['exp_avg'], state['exp_avg_sq']
                beta1, beta2 = group['betas']

                state['step'] += 1

                # Шаг Weight Decay в AdamW
                p.data.mul_(1 - group['lr'] * group['weight_decay'])

                # Обновление моментов
                exp_avg.mul_(beta1).add_(grad, alpha=1 - beta1)
                exp_avg_sq.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)

                bias_correction1 = 1 - beta1 ** state['step']
                bias_correction2 = 1 - beta2 ** state['step']

                step_size = group['lr'] / bias_correction1
                denom = (exp_avg_sq.sqrt() / torch.sqrt(torch.tensor(bias_correction2))) + group['eps']

                # Обновление весов
                p.data.addcdiv_(exp_avg, denom, value=-step_size)
        return loss


def plot_optimization(optimizer_class, title, start_pt, lr, n_iter=100, is_sgd=False, **kwargs):
    pt = torch.tensor(start_pt, requires_grad=True)
    if is_sgd:
        optimizer = optimizer_class([pt], lr=lr)
    else:
        optimizer = optimizer_class([pt], lr=lr, **kwargs)

    trace = [pt.clone().detach().numpy()]

    for _ in range(n_iter):
        optimizer.zero_grad()
        loss = objective(pt)
        loss.backward()
        optimizer.step()
        trace.append(pt.clone().detach().numpy())

    trace = np.array(trace)

    # Сетка для отображения контуров
    X = np.linspace(-20, 20, 800)
    Y = np.linspace(-50, 50, 800)
    X, Y = np.meshgrid(X, Y)
    Z = f_val(X, Y)

    plt.figure(figsize=(7, 5))
    levels = np.linspace(np.min(Z), np.max(Z), 50)
    cp = plt.contour(X, Y, Z, levels=levels, cmap='rainbow', alpha=0.5)
    plt.clabel(cp, inline=True, fontsize=8, fmt='%.1f')

    # Отрисовка траектории
    plt.plot(trace[:, 0], trace[:, 1], 'r.-', markersize=6, linewidth=1.5, label='Траектория')
    plt.plot(1, -7.5, 'g*', markersize=10, label='Седловая точка')
    plt.plot(-99 / 16, 50, 'b*', markersize=10, label='Глобальный минимум')


    # plt.title(f"{title} (lr={lr})")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim([-20, 20])  # Ограничиваем область обзора, чтобы сфокусироваться на траектории
    plt.ylim([-50, 50])
    plt.legend(loc='lower right', framealpha=0.9)
    plt.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()  # Компактный режим графика
    plt.show()


# ==========================================

print("=== Задание 1. Строим линии уровня ===")
plot_function_contours()

print("=== Задание 2. Траектории оптимизаторов ===")
# 2.1 Чистый градиентный спуск (GD) "застревает" в седловой точке.
# Примечание: torch.optim.SGD без momentum на аналитической функции
# работает как классический чистый градиентный спуск (GD).
# plot_optimization(
#     torch.optim.SGD,
#     "Градиентный спуск (GD) - сходимость к седлу",
#     [1.05, 10.0],
#     lr=0.5,
#     is_sgd=True
# )

plot_optimization(
    CustomGD,
    "Градиентный спуск GD - сходимость к седлу",
    [1.05, 10.0],
    lr=0.5
)

# 2.2 AdamW преодолевает седловую точку (гладкое движение)
plot_optimization(
    CustomAdamW,
    "Custom AdamW - пролет седловой точки",
    [1.05, 10.0],
    lr=0.5
)

# 2.3 AdamW Пилообразная ломаная (завышенный lr и низкие моменты)
plot_optimization(
    CustomAdamW,
    "Custom AdamW - пилообразная ломаная",
    [1.05, 10.0],
    lr=2.5,
    betas=(0.5, 0.9)
)

# 2.4 Встроенный PyTorch AdamW (для проверки)
plot_optimization(
    torch.optim.AdamW,
    "PyTorch AdamW",
    [1.05, 10.0],
    lr=0.5
)

# ==========================================
# Задание 3: Машинное обучение на датасете
# ==========================================

print("\n=== Задание 3. Обучение нейросети ===")

df = pd.read_csv('../data/playlist_2010to2023.csv', encoding='latin-1')
# Для примера берем только числовые фичи:
features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
df = df.dropna(subset=features + ['track_popularity'])
X = df[features].values
# Задача классификации: популярность > 70
y = (df['track_popularity'].values > 70).astype(np.float32)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train_t = torch.tensor(X_train, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
X_test_t = torch.tensor(X_test, dtype=torch.float32)
y_test_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)


class SpotifyNet(torch.nn.Module):
    def __init__(self, input_dim):
        super(SpotifyNet, self).__init__()
        self.fc1 = torch.nn.Linear(input_dim, 32)
        self.fc2 = torch.nn.Linear(32, 16)
        self.fc3 = torch.nn.Linear(16, 1)
        self.relu = torch.nn.ReLU()
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):
        return self.sigmoid(self.fc3(self.relu(self.fc2(self.relu(self.fc1(x))))))


def train_model(optimizer_class, name, **optim_params):
    torch.manual_seed(42)
    model = SpotifyNet(X_train_t.shape[1])
    criterion = torch.nn.BCELoss()
    optimizer = optimizer_class(model.parameters(), **optim_params)

    epochs = 200
    test_losses = []

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        loss = criterion(model(X_train_t), y_train_t)
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            test_loss = criterion(model(X_test_t), y_test_t)
            test_losses.append(test_loss.item())

    print(f"[{name}] Final Test Loss: {test_losses[-1]:.4f}")
    return test_losses, model


test_pt, model_pt = train_model(torch.optim.AdamW, "PyTorch AdamW", lr=0.001, weight_decay=1e-3)
test_cust, model_cust = train_model(CustomAdamW, "Custom AdamW", lr=0.001, weight_decay=1e-3)

plt.figure(figsize=(7, 4))
plt.plot(test_pt, label='PyTorch AdamW', linestyle='--', linewidth=3)
plt.plot(test_cust, label='Custom AdamW', alpha=0.7, linewidth=2)
# plt.title('Сравнение loss оптимизаторов на тестовой выборке')
plt.xlabel('Эпоха')
plt.ylabel('BCE Loss')
plt.legend()
plt.grid(True, linestyle=':')
plt.tight_layout()
plt.show()

# === ОЦЕНКА РЕЗУЛЬТАТОВ НА ТЕСТОВОЙ ВЫБОРКЕ ===
print("\n=== Оценка качества модели ===")

# Переводим модель в режим оценки (отключаем градиенты)
model_pt.eval()
with torch.no_grad():
    # Модель выдает вероятности от 0 до 1 (из-за Sigmoid)
    y_pred_probs = model_pt(X_test_t)

    # Если вероятность > 0.5, считаем что класс 1 (хит), иначе 0
    y_pred_classes = (y_pred_probs > 0.5).float()

# Переводим тензоры обратно в numpy массивы для sklearn
y_true = y_test_t.numpy()
y_pred = y_pred_classes.numpy()

# Считаем метрики
acc = accuracy_score(y_true, y_pred)
print(f"Accuracy (Доля правильных ответов): {acc * 100:.2f}%")

print("\nПодробный отчет (Classification Report):")
print(classification_report(y_true, y_pred, target_names=["Не хит (0)", "Хит (1)"]))

# По желанию: рисуем матрицу ошибок
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["Не хит", "Хит"], yticklabels=["Не хит", "Хит"])
# plt.title("Матрица ошибок (Confusion Matrix)")
plt.ylabel('Истинный класс')
plt.xlabel('Предсказанный класс')
plt.show()