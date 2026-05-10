import matplotlib.pyplot as plt
import numpy as np

# ex1
x_cond = np.array([2.8, 4.3, 8.2, 12.1, 16.6, 20.4, 23.8])
phi_cond = np.array([1.42, 2.84, 4.36, 5.93, 7.63, 9.40, 11.24])

# ex2
x_ring = np.array([2.5, 4.1, 5.4, 6.9, 7.8, 8.3, 8.8, 9, 21, 21.2, 21.5, 22.1, 23.6, 24.8, 26.2, 27.4])
phi_ring = np.array([1.77, 2.70, 3.60, 4.44, 5.14, 5.68, 6.26, 6.56, 6.56, 6.70, 7.24, 7.93, 8.76, 9.72, 10.74, 11.80])


a = np.sum(x_cond * phi_cond) / np.sum(x_cond**2)
x_mhk = np.linspace(2, 25, 100)
phi_mhk = a * x_mhk

plt.figure(figsize=(10, 7))

plt.plot(x_mhk, phi_mhk, 'b--', label=f'Плоский конденсатор', linewidth=1.5)
plt.scatter(x_cond, phi_cond, color='blue', s=40, zorder=3) #, label='Измерения (конденсатор)')

plt.plot(x_ring, phi_ring, 'rs-', label='Конденсатор с кольцом', markersize=4, linewidth=1, alpha=0.8)

# a, b = np.polyfit(x_cond, phi_cond, 1)
# phi_mhk = a * x_cond + b

# plt.figure(figsize=(10, 7))
# plt.scatter(x_cond, phi_cond, color='blue', s=40, zorder=3)
# plt.plot(x_cond, phi_mhk, 'b--', label=f'Конденсатор (МНК): $\phi = {a:.3f}x + {b:.3f}$', linewidth=1.5)

# plt.plot(x_ring, phi_ring, 'rs-', label='Конденсатор с кольцом', markersize=4, linewidth=1, alpha=0.8)

plt.xlabel('$x$, см', fontsize=12)
plt.ylabel('$\phi$, В', fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.5)

plt.xticks(np.arange(0, 31, 2))
plt.yticks(np.arange(0, 15, 1))
plt.xlim(0, 30)
plt.ylim(0, 14)

plt.legend(fontsize=10, loc='upper left')

plt.savefig('../img/graph_mnk.png', dpi=300)
plt.show()
