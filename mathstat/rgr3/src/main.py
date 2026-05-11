import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats

# 1. Загрузка данных
# Убедитесь, что файл RGR3_A_7.csv находится в той же папке, что и скрипт
data = pd.read_csv('../data/RGR3_A_7.csv')
x = data['x'].values
y = data['y'].values
n = len(x)
x_star = 9.3280

print(f"Загружено наблюдений: n = {n}")

# --- ФУНКЦИИ МЕТРИК ---
def get_metrics(y_true, y_pred, n_params):
    rss = np.sum((y_true - y_pred)**2)
    tss = np.sum((y_true - np.mean(y_true))**2)
    r2 = 1 - rss/tss
    rmse = np.sqrt(rss / len(y_true))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return r2, rmse, mape, rss

# --- 1. ЛИНЕЙНАЯ МОДЕЛЬ (y = a + bx) ---
X_lin = sm.add_constant(x)
model_lin = sm.OLS(y, X_lin).fit()
a_lin, b_lin = model_lin.params
y_pred_lin = model_lin.predict(X_lin)
r2_l, rmse_l, mape_l, rss_l = get_metrics(y, y_pred_lin, 2)
y_star_lin = a_lin + b_lin * x_star

# Статистический блок для линейной модели
s2_lin = rss_l / (n - 2)
s_lin = np.sqrt(s2_lin)
ci_lin = model_lin.conf_int(alpha=0.05) # 95% ДИ

# --- 2. КВАДРАТИЧНАЯ МОДЕЛЬ (y = a + bx + cx^2) ---
# Используем numpy.polyfit для удобства
coeffs_quad = np.polyfit(x, y, 2) # возвращает [c, b, a]
c_q, b_q, a_q = coeffs_quad
y_pred_quad = a_q + b_q*x + c_q*x**2
r2_q, rmse_q, mape_q, rss_q = get_metrics(y, y_pred_quad, 3)
y_star_quad = a_q + b_q*x_star + c_q*x_star**2

# --- 3. СТЕПЕННАЯ МОДЕЛЬ (y = a * x^b) ---
# Линеаризация: ln(y) = ln(a) + b*ln(x)
ln_x = np.log(x)
ln_y = np.log(y)
X_pow = sm.add_constant(ln_x)
model_pow = sm.OLS(ln_y, X_pow).fit()
ln_a_p, b_p = model_pow.params
a_p = np.exp(ln_a_p)
y_pred_pow = a_p * (x**b_p)
r2_p, rmse_p, mape_p, rss_p = get_metrics(y, y_pred_pow, 2)
y_star_pow = a_p * (x_star**b_p)

# --- ВЫВОД РЕЗУЛЬТАТОВ ---
print("\n" + "="*30)
print("РЕЗУЛЬТАТЫ РАСЧЕТОВ")
print("="*30)

print(f"\n1. ЛИНЕЙНАЯ МОДЕЛЬ: y = {a_lin:.4f} + {b_lin:.4f}*x")
print(f"   R^2: {r2_l:.4f}, RMSE: {rmse_l:.4f}, MAPE: {mape_l:.2f}%")
print(f"   Прогноз hat(y)({x_star}): {y_star_lin:.4f}")
print(f"   RSS: {rss_l:.4f}, s^2: {s2_lin:.4f}")
print(f"   95% ДИ для a: [{ci_lin[0][0]:.4f}, {ci_lin[0][1]:.4f}]")
print(f"   95% ДИ для b: [{ci_lin[1][0]:.4f}, {ci_lin[1][1]:.4f}]")
print(f"   t-статистика для b: {model_lin.tvalues[1]:.4f}, p-value: {model_lin.pvalues[1]:.6f}")

print(f"\n2. КВАДРАТИЧНАЯ МОДЕЛЬ: y = {a_q:.4f} + {b_q:.4f}*x + ({c_q:.4f})*x^2")
print(f"   R^2: {r2_q:.4f}, RMSE: {rmse_q:.4f}, MAPE: {mape_q:.2f}%")
print(f"   Прогноз hat(y)({x_star}): {y_star_quad:.4f}")

print(f"\n3. СТЕПЕННАЯ МОДЕЛЬ: y = {a_p:.4f} * x^{b_p:.4f}")
print(f"   R^2: {r2_p:.4f}, RMSE: {rmse_p:.4f}, MAPE: {mape_p:.2f}%")
print(f"   Прогноз hat(y)({x_star}): {y_star_pow:.4f}")

# --- ДИАГРАММА РАССЕЯНИЯ ---
plt.figure(figsize=(12, 7))
plt.scatter(x, y, color='gray', edgecolor='black', alpha=0.7, s=40)

# plt.title('Диаграмма рассеяния', fontsize=14)
plt.xlabel('x (Число ядер)', fontsize=12)
plt.ylabel('y (TDP, Вт)', fontsize=12)
# Настройка сетки для наглядности
plt.grid(True, linestyle=':', alpha=0.6)
# Добавим текстовое примечание (необязательно, для красоты)
plt.tight_layout()
plt.show()


# --- ПОСТРОЕНИЕ ГРАФИКОВ ---
plt.figure(figsize=(12, 7))
# 1. Диаграмма рассеяния
plt.scatter(x, y, color='gray', alpha=0.5, label='Исходные данные')
# 2. Линии регрессии
x_range = np.linspace(min(x), max(x), 500)
plt.plot(x_range, a_lin + b_lin*x_range, 'r-', label=f'Линейная (R²={r2_l:.2f})')
plt.plot(x_range, a_q + b_q*x_range + c_q*x_range**2, 'g-', label=f'Квадратичная (R²={r2_q:.2f})')
plt.plot(x_range, a_p * (x_range**b_p), 'b-', label=f'Степенная (R²={r2_p:.2f})')

# 3. Точка прогноза
plt.scatter([x_star], [y_star_quad], color='black', zorder=5)
# plt.annotate(f'Прогноз (Квадр.): {y_star_quad:.2f}', (x_star, y_star_quad), xytext=(10, 10), textcoords='offset points')

# plt.title('Сравнение регрессионных моделей')
plt.xlabel('x (Число ядер)')
plt.ylabel('y (TDP, Вт)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --- АНАЛИЗ ОСТАТКОВ (для линейной модели) ---
plt.figure(figsize=(12, 7))
plt.scatter(x, model_lin.resid, color='red', alpha=0.6)
plt.axhline(0, color='black', linestyle='--')
# plt.title('График остатков линейной модели')
plt.xlabel('x (Число ядер)')
plt.ylabel('e (Остатки)')
plt.grid(True)
plt.tight_layout()
plt.show()

# --- АНАЛИЗ ОСТАТКОВ (для квадратичной модели) ---
plt.figure(figsize=(12, 7))
# Расчет остатков: Реальное y минус предсказанное квадратичной моделью
resid_quad = y - y_pred_quad
plt.scatter(x, resid_quad, color='green', alpha=0.6)
plt.axhline(0, color='black', linestyle='--')
plt.xlabel('x (Число ядер)')
plt.ylabel('e (Остатки)')
plt.grid(True)
plt.tight_layout()
plt.show()

# --- АНАЛИЗ ОСТАТКОВ (для степенной модели) ---
plt.figure(figsize=(12, 7))
# Расчет остатков: Реальное y минус предсказанное степенной моделью
resid_pow = y - y_pred_pow
plt.scatter(x, resid_pow, color='blue', alpha=0.6)
plt.axhline(0, color='black', linestyle='--')
plt.xlabel('x (Число ядер)')
plt.ylabel('e (Остатки)')
plt.grid(True)
plt.tight_layout()
plt.show()