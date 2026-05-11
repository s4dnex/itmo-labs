import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 1. Загрузка данных
df = pd.read_csv('../data/variant_7.csv')
n = len(df)
x = df['x'].values
y = df['y'].values

# 4.1. Средние значения
x_mean = np.mean(x)
y_mean = np.mean(y)

# 4.2. Вспомогательные суммы
Sxx = np.sum((x - x_mean)**2)
Sxy = np.sum((x - x_mean) * (y - y_mean))

# 4.3. Оценки коэффициентов
beta1_hat = Sxy / Sxx
beta0_hat = y_mean - beta1_hat * x_mean

# 4.4. Прогнозные значения и остатки
y_pred = beta0_hat + beta1_hat * x
residuals = y - y_pred

# 4.5. Остаточная сумма квадратов
RSS = np.sum(residuals**2)

# 4.10. Коэффициент детерминации
TSS = np.sum((y - y_mean)**2)
R2 = 1 - (RSS / TSS)

# 4.6. Оценка дисперсии
s2 = RSS / (n - 2)
s = np.sqrt(s2)

# 4.7. Стандартные ошибки
se_beta1 = s / np.sqrt(Sxx)
se_beta0 = s * np.sqrt(1/n + x_mean**2 / Sxx)

# 4.8. Доверительные интервалы для коэффициентов (alpha = 0.05)
t_crit = stats.t.ppf(1 - 0.025, n - 2)
ci_beta0 = (beta0_hat - t_crit * se_beta0, beta0_hat + t_crit * se_beta0)
ci_beta1 = (beta1_hat - t_crit * se_beta1, beta1_hat + t_crit * se_beta1)

# Вывод результатов для отчета
print(f"--- Результаты расчетов ---")
print(f"n = {n}")
print(f"x_mean = {x_mean:.4f}, y_mean = {y_mean:.4f}")
print(f"Sxx = {Sxx:.4f}, Sxy = {Sxy:.4f}")
print(f"beta1_hat = {beta1_hat:.4f}, beta0_hat = {beta0_hat:.4f}")
print(f"RSS = {RSS:.4f}, TSS = {TSS:.4f}, R2 = {R2:.4f}")
print(f"s^2 = {s2:.4f}, s = {s:.4f}")
print(f"SE(beta1) = {se_beta1:.4f}, SE(beta0) = {se_beta0:.4f}")
print(f"t_crit = {t_crit:.4f}")
print(f"CI beta0: [{ci_beta0[0]:.4f}, {ci_beta0[1]:.4f}]")
print(f"CI beta1: [{ci_beta1[0]:.4f}, {ci_beta1[1]:.4f}]")

# Построение графика
x_range = np.linspace(min(x), max(x), 100)
y_range_pred = beta0_hat + beta1_hat * x_range

# SE для функции регрессии
se_y = s * np.sqrt(1/n + (x_range - x_mean)**2 / Sxx)
y_ci_upper = y_range_pred + t_crit * se_y
y_ci_lower = y_range_pred - t_crit * se_y

plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', label='Исходные данные', alpha=0.6)
plt.plot(x_range, y_range_pred, color='red', label='Линия регрессии')
plt.fill_between(x_range, y_ci_lower, y_ci_upper, color='red', alpha=0.1, label='95% Дов. интервал')
plt.xlabel('x')
plt.ylabel('y')
# plt.title('Простая линейная регрессия с доверительным интервалом')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('../img/regression_plot.png')
plt.show()

# Создание таблицы остатков для Typst
res_df = pd.DataFrame({
    'i': df['i'],
    'xi': x,
    'yi': y,
    'yi_hat': y_pred,
    'ei': residuals
})
print("\n--- Первые 5 строк таблицы остатков ---")
print(res_df.head().to_string(index=False))