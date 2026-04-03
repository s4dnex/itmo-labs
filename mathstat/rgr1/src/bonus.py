import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew

df = pd.read_csv('../data/RGR1_A-7_X1-X4.csv')
x4 = df['X4'].values

def cluster_x4(data, c1_init, c2_init, tol=0.01):
    c1, c2 = c1_init, c2_init
    iteration = 0
    stable = False

    print(f"Начальные центры: c1 = {c1}, c2 = {c2}")

    while not stable:
        iteration += 1
        # map data to corresponding centers
        group1 = data[np.abs(data - c1) < np.abs(data - c2)]
        group2 = data[np.abs(data - c1) >= np.abs(data - c2)]

        # recalculate centers
        new_c1 = np.mean(group1)
        new_c2 = np.mean(group2)

        print(f"Итерация {iteration}: c1 = {new_c1:.2f}, c2 = {new_c2:.2f} (n1={len(group1)}, n2={len(group2)})")

        # stabilization check
        if np.abs(new_c1 - c1) < tol and np.abs(new_c2 - c2) < tol:
            stable = True

        c1, c2 = new_c1, new_c2

    return group1, group2, c1, c2


g1, g2, center1, center2 = cluster_x4(x4, 40, 110)

def get_stats(group):
    return {
        'n': len(group),
        'mean': np.mean(group),
        'median': np.median(group),
        'std': np.std(group, ddof=1),
        'skew': skew(group)
    }

s1 = get_stats(g1)
s2 = get_stats(g2)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.hist(g1, bins='sturges', color='skyblue', edgecolor='black', alpha=0.7)
ax1.axvline(s1['mean'], color='red', label='Среднее')
ax1.axvline(s1['median'], color='green', linestyle='--', label='Медиана')
ax1.set_title(f'Группа 1 (Центр ~{center1:.1f})')
ax1.legend()

ax2.hist(g2, bins='sturges', color='salmon', edgecolor='black', alpha=0.7)
ax2.axvline(s2['mean'], color='red', label='Среднее')
ax2.axvline(s2['median'], color='green', linestyle='--', label='Медиана')
ax2.set_title(f'Группа 2 (Центр ~{center2:.1f})')
ax2.legend()

plt.tight_layout()
plt.savefig("../img/x4_clusters.png")