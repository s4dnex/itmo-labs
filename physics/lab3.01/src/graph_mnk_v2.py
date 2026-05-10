import matplotlib.pyplot as plt
import numpy as np

# ex1 (плоский конденсатор)
x_cond = np.array([2.8, 4.3, 8.2, 12.1, 16.6, 20.4, 23.8])
phi_cond = np.array([1.42, 2.84, 4.36, 5.93, 7.63, 9.40, 11.24])

# ex2 (конденсатор с кольцом)
x_ring = np.array([2.5, 4.1, 5.4, 6.9, 7.8, 8.3, 8.8, 9, 21, 21.2, 21.5, 22.1, 23.6, 24.8, 26.2, 27.4])
phi_ring = np.array([1.77, 2.70, 3.60, 4.44, 5.14, 5.68, 6.26, 6.56, 6.56, 6.70, 7.24, 7.93, 8.76, 9.72, 10.74, 11.80])


# 1. МНК для плоского конденсатора (через ноль)
a_cond = np.sum(x_cond * phi_cond) / np.sum(x_cond**2)
x_mhk_cond = np.linspace(0, 26, 100)
phi_mhk_cond = a_cond * x_mhk_cond

# 2. МНК для области ДО кольца
x_left = x_ring[x_ring <= 9]
phi_left = phi_ring[x_ring <= 9]
a_left = np.sum(x_left * phi_left) / np.sum(x_left**2)
x_range_left = np.linspace(0, 9.5, 50)
phi_range_left = a_left * x_range_left

# 3. Область кольца (плато)
phi_plateau = 6.56
x_range_ring = np.linspace(9, 21, 10)
phi_range_ring = np.full_like(x_range_ring, phi_plateau)

# 4. МНК для области ПОСЛЕ кольца
x_right = x_ring[x_ring >= 21]
phi_right = phi_ring[x_ring >= 21]
a_right, b_right = np.polyfit(x_right, phi_right, 1)
x_range_right = np.linspace(20.75, 28, 50)
phi_range_right = a_right * x_range_right + b_right


plt.figure(figsize=(10, 7))
# ex1
plt.plot(x_mhk_cond, phi_mhk_cond, 'b--', label='Плоский конденсатор', linewidth=1.5, alpha=0.7)
plt.scatter(x_cond, phi_cond, color='blue', s=40, zorder=3, edgecolors='black')

# ex2 
# Левая ветка
plt.plot(x_range_left, phi_range_left, 'r--', linewidth=1.5)
# Плато (кольцо)
plt.plot(x_range_ring, phi_range_ring, 'r-', linewidth=2)
# Правая ветка
plt.plot(x_range_right, phi_range_right, 'r--', linewidth=1.5, label='Конденсатор с кольцом')
# Точки измерений
plt.scatter(x_ring, phi_ring, color='red', marker='s', s=30, zorder=3, alpha=0.8)
plt.xlabel('$x$, см', fontsize=12)
plt.ylabel('$\phi$, В', fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.4)
plt.xticks(np.arange(0, 31, 2))
plt.yticks(np.arange(0, 15, 1))
plt.xlim(0, 30)
plt.ylim(0, 14)
plt.legend(fontsize=10, loc='upper left')
# plt.title('Аппроксимация распределения потенциала $\phi(x)$', fontsize=13)
plt.savefig('../img/graph_mnk_v2.png', dpi=300)
plt.show()
