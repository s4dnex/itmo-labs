import numpy as np
import matplotlib.pyplot as plt

x = np.array([11.6,16.6,21.6,26.6,31.6,36.6]) 
y = np.array([160,200,240,280,320,360,400,440])

M = np.array([
    [1,4,5,0,0,0,0,0],
    [0,6,7,2,0,0,0,0],
    [0,0,5,8,6,0,0,0],
    [0,0,0,9,13,6,0,0],
    [0,0,0,0,7,8,4,0],
    [0,0,0,0,0,0,6,3],
], dtype=float)

n = int(M.sum())

mx = M.sum(axis=1)
my = M.sum(axis=0)

sum_mx_x = (mx * x).sum()
sum_my_y = (my * y).sum()

x_bar = sum_mx_x / n
y_bar = sum_my_y / n

sum_mx_x2 = (mx * x**2).sum()
sum_my_y2 = (my * y**2).sum()

sum_xy = 0.0
for i, xi in enumerate(x):
    for j, yj in enumerate(y):
        sum_xy += M[i, j] * xi * yj

s_x2 = (sum_mx_x2 - n * x_bar**2) / (n - 1)
s_y2 = (sum_my_y2 - n * y_bar**2) / (n - 1)
s_xy = (sum_xy - n * x_bar * y_bar) / (n - 1)

s_x = np.sqrt(s_x2)
s_y = np.sqrt(s_y2)
r = s_xy / (s_x * s_y)

b = s_xy / s_x2
a = y_bar - b * x_bar

xs = []
ys = []
for i, xi in enumerate(x):
    for j, yj in enumerate(y):
        cnt = int(M[i, j])
        if cnt > 0:
            xs.extend([xi]*cnt)
            ys.extend([yj]*cnt)
xs = np.array(xs)
ys = np.array(ys)

plt.figure(figsize=(9,6))
plt.scatter(xs, ys, s=25, alpha=0.8)
xx = np.linspace(x.min()-1, x.max()+1, 200)
yy = a + b * xx
plt.plot(xx, yy)
plt.xlabel('X (тыс. ден. ед.)')
plt.ylabel('Y (т)')
plt.grid(True)
plt.tight_layout()

out_path = '../images//regression_plot_corrected.png'
plt.savefig(out_path, dpi=150)
plt.show()