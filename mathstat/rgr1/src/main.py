import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../data/RGR1_A-7_X1-X4.csv')

def save_plots(column_name, filename):
    data = df[column_name].sort_values()
    n = len(data)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    y = np.arange(1, n + 1) / n
    ax1.step(data, y, where='post')
    ax1.set_title(f'ЭФР {column_name}')
    ax1.grid(True, linestyle=':')


    ax2.hist(data, bins='sturges', edgecolor='black', color='lightblue', alpha=0.7)
    ax2.axvline(data.mean(), color='red', linestyle='--', label='Среднее')
    ax2.axvline(data.median(), color='green', linestyle='-', label='Медиана')
    ax2.set_title(f'Гистограмма {column_name}')
    ax2.legend()

    plt.tight_layout()
    plt.savefig("../img/" + filename)
    plt.close()

save_plots('X1', 'x1_plots.png')
save_plots('X2', 'x2_plots.png')
save_plots('X3', 'x3_plots.png')
save_plots('X4', 'x4_plots.png')

stats = pd.DataFrame({
    'Среднее': df.mean(),
    'Медиана': df.median(),
    'Дисперсия (смещ.)': df.var(ddof=0),
    'Дисперсия (несмещ.)': df.var(ddof=1),
    'Минимум': df.min(),
    'Максимум': df.max()
})

print("Выборочные характеристики:")
print(stats.round(2))