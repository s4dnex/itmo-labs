import pandas as pd
import numpy as np
import warnings
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.ensemble import GradientBoostingRegressor

warnings.simplefilter(action='ignore')
df = pd.read_csv('../data/heart_2020_cleaned.csv').sample(n=5000, random_state=42)

target_col = 'BMI' # Регрессия: целевой признак - Индекс массы тела

label_encoders = {}
for col in df.columns:
    if not pd.api.types.is_numeric_dtype(df[col]):
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

X = df.drop(columns=[target_col])
y = df[target_col]

features_list = list(X.columns)

global N_START_FEATURES, N_END_FEATURES, NC_MAX, N_STEPS, INIT_PHEROMONE
global RO, EXPLOITATION_PROB, ALPHA, BETA, N_ANTS, all_scaled, sim

N_START_FEATURES = X.shape[1]  # 17 признаков
N_END_FEATURES = 8  # Отбираем 8 признаков
NC_MAX = 5  # Максимальное число циклов
N_STEPS = 8  # Число шагов внутри цикла
INIT_PHEROMONE = 0.2
RO = 0.2  # Коэффициент испарения
EXPLOITATION_PROB = 0.6  # Вероятность exploitation
ALPHA = 1.0
BETA = 1.0
N_ANTS = 10  # Число муравьев

scaler = MinMaxScaler()
all_scaled = scaler.fit_transform(X)

# ==========================================
# 2. ОТБОР ПРИЗНАКОВ: GRADIENT BOOSTING
# ==========================================
print(f"\nОбучение GradientBoostingRegressor (целевой признак: {target_col})...")
params = {
    "n_estimators": 300,
    "max_depth": 4,
    "min_samples_split": 10,
    "learning_rate": 0.01,
    "random_state": 42
}
gb_model = GradientBoostingRegressor(**params)
gb_model.fit(X, y)

# Получаем и сортируем топ-8 важных признаков
importances = gb_model.feature_importances_
gb_top_indices = np.argsort(importances)[::-1][:N_END_FEATURES]
gb_selected_features = set([features_list[i] for i in gb_top_indices])

print(f"Топ-{N_END_FEATURES} признаков (Gradient Boosting):")
print(gb_selected_features)

# ==========================================
# 3. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ И АЛГОРИТМ UFSACO
# ==========================================
sim = {}
def set_sim(i, j):
    a = all_scaled[:, i]
    b = all_scaled[:, j]
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        res = 0.0
    else:
        res = np.dot(np.asarray(a), np.asarray(b)) / (norm_a * norm_b)
    sim[(min(i, j), max(i, j))] = np.abs(res)
    return res


def get_sim(i, j):
    (i, j) = (min(i, j), max(i, j))
    if (i, j) not in sim.keys():
        set_sim(i, j)
    return max(sim[(i, j)], 1e-6)


def UFSACO(verbose=False):
    global tau
    tau = INIT_PHEROMONE * np.ones((N_START_FEATURES))

    for count in range(NC_MAX):
        ants_pos = np.random.choice(N_START_FEATURES, size=N_ANTS, p=tau / sum(tau))
        visits = np.zeros((N_START_FEATURES))
        nodes_visited = {(k, i): set() for k in range(N_ANTS) for i in range(N_START_FEATURES)}

        for iter in range(N_STEPS):
            for k in range(N_ANTS):
                i = ants_pos[k]
                visited = nodes_visited[(k, i)]
                unvisited = list((set(range(N_START_FEATURES)) - visited) - {i})

                if len(unvisited) == 0:
                    continue

                # Эвристика: tau / cos_sim. Чем меньше коллинеарность, тем выше желательность
                node_score = [tau[j] / np.power(get_sim(i, j), ALPHA) for j in unvisited]

                q = np.random.uniform()
                if q <= EXPLOITATION_PROB:
                    jj = np.argmax(node_score)
                else:
                    p = node_score / sum(node_score)
                    p = p / p.sum()
                    jj = np.random.choice(len(unvisited), size=1, p=p)[0]

                j = unvisited[jj]
                ants_pos[k] = j
                nodes_visited[(k, i)].add(j)
                visits[j] += 1

                if verbose:
                    print(f"count={count}, iter={iter}, k={k}, i={i}, j={j}")

        total_visits = sum(visits)
        if total_visits > 0:
            tau = (1 - RO) * tau + (visits / total_visits)
    return tau


# ==========================================
# 4. ЗАПУСК UFSACO С АВТОВАРЬИРОВАНИЕМ
# ==========================================
intersection = set()
attempt = 1

print("\nЗапуск алгоритма муравьиной колонии (UFSACO) без целевой переменной...")

while len(intersection) < 4 and attempt <= 15:
    print(f"\n--- Итерация автоподбора {attempt} ---")
    print(f"Параметры: Муравьев={N_ANTS}, Эпох={NC_MAX}, P_Exploit={EXPLOITATION_PROB:.2f}, Alpha={ALPHA:.2f}")

    # Запуск
    tau = UFSACO(verbose=False)

    # Извлечение топ-признаков на основе феромона
    features_UFSACO_idx = np.array(tau.argsort()[::-1][0:N_END_FEATURES])
    aco_selected_features = set([features_list[i] for i in features_UFSACO_idx])

    # Сравниваем
    intersection = gb_selected_features.intersection(aco_selected_features)

    print(f"Топ-{N_END_FEATURES} признаков (UFSACO):")
    print(aco_selected_features)
    print(f"Пересечение (Мощность = {len(intersection)}): {intersection}")

    if len(intersection) < 4:
        print("ВНИМАНИЕ: Мощность пересечения меньше 4. Варьируем гиперпараметры...")
        # 1. Снижаем влияние эвристики, чтобы муравьи меньше смотрели на редкие болезни
        ALPHA = max(0.0, ALPHA - 0.15)
        # 2. Снижаем вероятность жесткого выбора (Exploitation), даем больше случайности (Exploration)
        EXPLOITATION_PROB = max(0.1, EXPLOITATION_PROB - 0.1)
        # 3. Добавляем муравьев и эпох для лучшего закрепления феромона
        N_ANTS += 5
        NC_MAX += 2
    else:
        print("\nУсловие выполнено: пересечение состоит из 4 и более признаков.")

    attempt += 1

if len(intersection) < 4:
    print("\nИсчерпано количество попыток автоподбора. Метаэвристика не достигла пересечения >= 4.")