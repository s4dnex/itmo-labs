import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

df = pd.read_csv('../docs/stocks.csv', sep=';')
prices = df['<CLOSE>'].values
t = np.arange(len(prices))  # Временная шкала в днях

# Определение констант времени (в торговых днях)
time_constants = {
    "1 день": 1,
    "1 неделя": 5,
    "1 месяц": 21,
    "3 месяца": 63,
    "1 год": 252
}

fig, axes = plt.subplots(nrows=len(time_constants), ncols=1, figsize=(12, 20))
fig.subplots_adjust(hspace=0.4)
colors = ['blue', 'green', 'orange', 'red', 'purple']

for i, ((label, T), color) in enumerate(zip(time_constants.items(), colors)):
    # Настройка фильтра первого порядка W(p) = 1 / (Tp + 1)
    num = [1]
    den = [T, 1]
    filter1 = signal.TransferFunction(num, den)

    # Решение проблемы старта из нуля (задание начального состояния X0)
    # Устанавливаем выход фильтра в начальный момент равным первой цене
    tout, y, x_out = signal.lsim(filter1, U=prices, T=t, X0=[prices[0]])

    ax = axes[i]
    ax.plot(t, prices, label='Оригинал', color='black', alpha=0.8, lw=1)
    ax.plot(tout, y, label=f'Сглаживание (T = {label})', color=color, lw=2)

    ax.set_title(f'Сглаживание котировок акций Сбербанка: {label}', fontsize=12, fontweight='bold')
    ax.set_ylabel('Цена (руб.)')
    ax.set_xlabel('Торговые дни (от 01.01.2021 по 21.12.2025)')
    ax.legend(loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.6)

plt.show()