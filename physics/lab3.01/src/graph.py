import matplotlib.pyplot as plt
import numpy as np

# ex1
x_cond = [2.8, 4.3, 8.2, 12.1, 16.6, 20.4, 23.8]
phi_cond = [1.42, 2.84, 4.36, 5.93, 7.63, 9.40, 11.24]

# ex2
x_ring =    [2.5,    4.1,    5.4,   6.9,    7.8,    8.3,    8.8,    9,      21,     21.2,    21.5,   22.1,  23.6,   24.8,   26.2,   27.4]
phi_ring =  [1.77,   2.70,   3.60,  4.44,   5.14,   5.68,   6.26,   6.56,   6.56,   6.70,    7.24,   7.93,  8.76,   9.72,   10.74,  11.80]

plt.figure(figsize=(10, 6))

plt.plot(x_cond, phi_cond, 'bo-', label='Плоский конденсатор', markersize=4)
plt.plot(x_ring, phi_ring, 'rs-', label='Конденсатор с кольцом', markersize=4)

plt.xlabel('$x$, см')
plt.ylabel('$\phi$, В')
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend()

plt.xticks(np.arange(0, 31, 2))
plt.yticks(np.arange(0, 15, 1))

plt.savefig('../img/graph.png', dpi=300)
plt.show()
