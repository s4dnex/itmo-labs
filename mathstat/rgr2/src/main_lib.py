import pandas as pd
import numpy as np
from scipy import stats
df = pd.read_csv('..\\data\\data.csv', sep=';')

alpha = 0.05
n = len(df)
print(f"Объем выборки: n = {n}")
print("-" * 30)

# --- ЗАДАНИЕ 4.2: Параметрический критерий (X1 и X2) ---
# Гипотеза о равенстве средних (t-тест Стьюдента)
# По ключу equal_var предполагается равенство дисперсий
t_stat, p_val_t = stats.ttest_ind(df['X1'], df['X2'], equal_var=True)

print("4.2. Параметрический критерий (X1 vs X2):")
print(f"Среднее X1: {df['X1'].mean():.2f}, Среднее X2: {df['X2'].mean():.2f}")
print(f"Наблюдаемое значение t-статистики: {t_stat:.3f}")
print(f"p-value: {p_val_t:.4f}")
if p_val_t < alpha:
    print("Результат: H0 отвергается")
else:
    print("Результат: H0 не отвергается")
print("-" * 30)


# --- ЗАДАНИЕ 4.3: Гипотеза о параметре распределения (X3) ---
# Проверка H0: mu = 86.80
mu_0 = 86.80
t_stat_x3, p_val_x3 = stats.ttest_1samp(df['X3'], mu_0)

print("4.3. Проверка гипотезы о матожидании X3:")
print(f"H0: mu = {mu_0}")
print(f"Среднее X3 по выборке: {df['X3'].mean():.2f}")
print(f"Наблюдаемое значение t-статистики: {t_stat_x3:.3f}")
print(f"p-value: {p_val_x3:.4f}")
if p_val_x3 < alpha:
    print("Результат: H0 отвергается")
else:
    print("Результат: H0 не отвергается")
print("-" * 30)


# --- ЗАДАНИЕ 4.4: Непараметрический критерий (X1 и X2) ---
# Критерий Манна-Уитни
u_stat, p_val_u = stats.mannwhitneyu(df['X1'], df['X2'], alternative='two-sided')

print("4.4. Критерий Манна-Уитни (X1 vs X2):")
print(f"Статистика U: {u_stat:.2f}")
print(f"p-value: {p_val_u:.4f}")
if p_val_u < alpha:
    print("Результат: H0 отвергается (распределения различны)")
else:
    print("Результат: H0 не отвергается")
print("-" * 30)


# --- ЗАДАНИЕ 4.5: Критерий согласия Пирсона (X4) ---
# Проверка на экспоненциальное распределение с lambda = 0.053
lam = 0.053

bins = [0, 4.19, 9.59, 17.20, 30.21, np.inf]

# Наблюдаемые частоты
f_obs, _ = np.histogram(df['X4'], bins=bins)

# Теоретические вероятности для экспоненциального закона: F(x) = 1 - exp(-lambda * x)
# Вероятность попадания в интервал [a, b] = F(b) - F(a) = exp(-lambda*a) - exp(-lambda*b)
def exp_cdf(x):
    return 1 - np.exp(-lam * x)

probabilities = []
for i in range(len(bins)-1):
    p = exp_cdf(bins[i+1]) - exp_cdf(bins[i])
    probabilities.append(p)

# Ожидаемые частоты
f_exp = np.array(probabilities) * n

# Расчет статистики Хи-квадрат
chi2_stat, p_val_chi2 = stats.chisquare(f_obs, f_exp)

print("4.5. Критерий согласия Пирсона (X4):")
print(f"Наблюдаемые частоты: {f_obs}")
print(f"Ожидаемые частоты:   {f_exp.round(2)}")
print(f"Статистика Хи-квадрат: {chi2_stat:.3f}")
print(f"p-value: {p_val_chi2:.4f}")
if p_val_chi2 < alpha:
    print("Результат: H0 отвергается (данные не соответствуют Exp)")
else:
    print("Результат: H0 не отвергается (данные согласуются с моделью)")