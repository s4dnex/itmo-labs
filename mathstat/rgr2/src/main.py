import math
import csv

data = {'X1': [], 'X2': [], 'X3': [], 'X4': []}
with open('..\\data\\data.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        for col in data:
            data[col].append(float(row[col]))

n = len(data['X1'])

# Выборочное среднее: X_bar = (1/n) * sum(x_i)
def get_mean(sample):
    return sum(sample) / len(sample)

# Исправленная выборочная дисперсия: s^2 = (1/(n-1)) * sum((x_i - x_bar)^2)
def get_variance(sample):
    mean = get_mean(sample)
    return sum((x - mean)**2 for x in sample) / (len(sample) - 1)

# --- ЗАДАНИЕ 4.2: t-критерий Стьюдента для двух выборок ---
m1 = get_mean(data['X1'])
m2 = get_mean(data['X2'])
v1 = get_variance(data['X1'])
v2 = get_variance(data['X2'])

# Объединенная дисперсия: ((n-1)*s1^2 + (m-1)*s2^2) / (n + m - 2)
combined_v = ((n - 1) * v1 + (n - 1) * v2) / (n + n - 2)

# Статистика: h = (x_bar - y_bar) / (sigma * sqrt(1/n + 1/m))
h_42 = (m1 - m2) / (math.sqrt(combined_v) * math.sqrt(1 / n + 1 / n))

print(f"4.2. Параметрический критерий (X1, X2):")
print(f"   Средние: X1={m1:.2f}, X2={m2:.2f}")
print(f"   Объединенная дисперсия: {combined_v:.2f}")
print(f"   Наблюдаемое значение h: {h_42:.3f}")


# --- ЗАДАНИЕ 4.3: t-критерий для одной выборки (X3) ---
mu_0 = 86.80
m3 = get_mean(data['X3'])
s3 = math.sqrt(get_variance(data['X3']))

# h = sqrt(n) * (x_bar - mu_0) / s
h_43 = math.sqrt(n) * (m3 - mu_0) / s3

print(f"\n4.3. Проверка гипотезы о параметре (X3):")
print(f"   H0: mu = {mu_0}")
print(f"   Среднее X3: {m3:.2f}, s: {s3:.2f}")
print(f"   Наблюдаемое значение h: {h_43:.3f}")


# --- ЗАДАНИЕ 4.4: Критерий Манна-Уитни (X1, X2) ---
combined = []
for x in data['X1']: combined.append((x, 'X1'))
for x in data['X2']: combined.append((x, 'X2'))

# Сортируем для присвоения рангов
combined.sort(key=lambda it: it[0])

ranks_x1 = 0
for rank, (val, group) in enumerate(combined, 1):
    if group == 'X1':
        ranks_x1 += rank

# Статистика U = R_x - (m*(m+1))/2
u_stat = ranks_x1 - (n * (n + 1)) / 2

# Z-критерий:
expected_u = (n * n) / 2
sigma_u = math.sqrt((n * n * (n + n + 1)) / 12)
z_score = (u_stat - expected_u) / sigma_u

print(f"\n4.4. Непараметрический критерий (X1, X2):")
print(f"   Сумма рангов X1: {ranks_x1}")
print(f"   Статистика U: {u_stat:.1f}")
print(f"   Z-статистика: {z_score:.3f}")


# --- ЗАДАНИЕ 4.5: Критерий согласия Пирсона (X4) ---
lam = 0.053
bins = [0, 4.19, 9.59, 17.20, 30.21, float('inf')]

# Наблюдаемые частоты
n_k = [0] * (len(bins) - 1)
for x in data['X4']:
    for i in range(len(bins)-1):
        if bins[i] <= x < bins[i+1]:
            n_k[i] += 1
            break

# Теоретические вероятности: F(x) = 1 - e^(-lam*x)
def exp_cdf(x):
    if x == float('inf'): return 1.0
    return 1 - math.exp(-lam * x)

p_k = []
for i in range(len(bins)-1):
    prob = exp_cdf(bins[i+1]) - exp_cdf(bins[i])
    p_k.append(prob)

# Статистика Хи-квадрат: sum( (nk - n*pk)^2 / (n*pk) )
chi2_val = 0
print(f"\n4.5. Критерий согласия (X4):")
print(f"   Интервал | n_k | n*p_k")
for i in range(len(n_k)):
    expected = n * p_k[i]
    chi2_val += ((n_k[i] - expected)**2) / expected
    print(f"   {i+1}        | {n_k[i]}  | {expected:.2f}")

print(f"   Наблюдаемое значение Chi2: {chi2_val:.3f}")