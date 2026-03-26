import matplotlib.pyplot as plt
import numpy as np

# data
bins = [24, 31, 39, 46, 54, 61, 69, 77, 84]
counts = [11, 26, 27, 15, 11, 18, 5, 7]
widths = np.diff(bins)
centers = [bins[i] + widths[i]/2 for i in range(len(widths))]

x_bar = 48.68  # avg
median = 45.2  # median
sigma = 14.88  # std dev
interval = [x_bar - sigma, x_bar + sigma]

plt.figure(figsize=(10, 5))

# histogram
bars = plt.bar(centers, counts, width=widths, color='#6394be', edgecolor='black', alpha=0.9)

# freqs
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom', fontweight='bold', size=9)

# median line
plt.axvline(median, color='green', linestyle='--', linewidth=2.5, label=f'Медиана = {median}')

# avg line
plt.axvline(x_bar, color='red', linestyle='-', linewidth=2, label=f'Среднее x̄ = {x_bar:.2f}')

# [x-sigma, x+sigma] 
plt.axvspan(interval[0], interval[1], color='red', alpha=0.15, label=f'Интервал [x̄ - σ; x̄ + σ]')
plt.axvline(interval[0], color='red', linestyle=':', linewidth=1.5, alpha=0.6)
plt.axvline(interval[1], color='red', linestyle=':', linewidth=1.5, alpha=0.6)

plt.xlabel('Значение признака', size=11)
plt.ylabel('Частота', size=11)
plt.xticks(bins, rotation=45)
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.legend()

plt.tight_layout()
plt.savefig('../img/histogram.png', dpi=300)
plt.show()