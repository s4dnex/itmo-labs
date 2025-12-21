import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# 1. Загрузка данных
df = pd.read_csv('../docs/stocks.csv', sep=';')
prices = df['<CLOSE>'].values
t = np.arange(len(prices))  # Временная ось в днях

# 2. Определение параметров фильтрации (в торговых днях)
time_constants = {
    "1 день": 1,
    "1 неделя": 5,
    "1 месяц": 21,
    "3 месяца": 63,
    "1 год": 252
}

plt.figure(figsize=(14, 8))
plt.plot(t, prices, label='Исходные данные (SBER)', color='lightgray', alpha=0.7, lw=1)

colors = ['blue', 'green', 'orange', 'red', 'purple']

# 3. Применение фильтра для каждого T
for (label, T), color in zip(time_constants.items(), colors):
    # W(p) = 1 / (Tp + 1)
    num = [1]
    den = [T, 1]
    sys = signal.TransferFunction(num, den)

    # Решение проблемы "старта из нуля":
    # Задаем начальное состояние X0 равным первой цене.
    tout, y, xout = signal.lsim(sys, U=prices, T=t, X0=[prices[0]])

    plt.plot(tout, y, label=f'T = {label}', color=color, lw=2)

# Оформление графика
plt.title('Сглаживание котировок акций Сбербанка (Линейная фильтрация 1-го порядка)', fontsize=14)
plt.xlabel('Торговые дни (с 04.01.2021)', fontsize=12)
plt.ylabel('Цена закрытия (руб.)', fontsize=12)
plt.legend()
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.show()