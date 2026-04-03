import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('../data/RGR1_A-7_X1-X4.csv')
n = len(df)

# 4.3
# X1
x1 = df['X1']
s_val = x1.std(ddof=0)
m_val = x1.mean()

a_mm = m_val - np.sqrt(3) * s_val
b_mm = m_val + np.sqrt(3) * s_val

a_mmp = x1.min()
b_mmp = x1.max()
print(f"X1 ММ:  a={a_mm:.2f}, b={b_mm:.2f}")
print(f"X1 ММП: a={a_mmp:.2f}, b={b_mmp:.2f}")

# X2
x2 = df['X2']

c_mm = x2.mean() - x2.std(ddof=0)
lambda_mm = 1 / x2.std(ddof=0)

c_mmp = x2.min()
lambda_mmp = 1 / (x2.mean() - c_mmp)

print(f"X2 ММ:  c={c_mm:.2f}, lambda={lambda_mm:.4f}")
print(f"X2 ММП: c={c_mmp:.2f}, lambda={lambda_mmp:.4f}")

# X3
x3 = df['X3']
mu_mmp = x3.mean()
s2_mmp = x3.var(ddof=0)

print(f"X3: hat_mu = {mu_mmp:.4f}, hat_sigma^2 = {s2_mmp:.4f}")


# 4.4
print()
n = len(df)
cols = ['X1', 'X2', 'X3']

print(f"{'Столбец':<10} | {'x0':<8} | {'P_эмп':<10} | {'P_парам':<10}")
print("-" * 50)

results_prob = {}
results_grouped = {}

for col in cols:
    data = df[col]
    x_bar = data.mean()
    s_std = data.std(ddof=1)

    x0 = x_bar + s_std

    # P(X > x0)
    emp_p = len(data[data > x0]) / n

    if col == 'X1':  # ММП: a=min, b=max
        a, b = data.min(), data.max()
        param_p = (b - x0) / (b - a) if x0 < b else 0
    elif col == 'X2':  # ММП: c=min, lambda=1/(mean-c)
        c = data.min()
        lmbd = 1 / (x_bar - c)
        param_p = np.exp(-lmbd * (x0 - c))
    else:  # ММП: mu=mean, sigma=std(ddof=0)
        param_p = 1 - stats.norm.cdf(x0, loc=x_bar, scale=data.std(ddof=0))

    results_prob[col] = (x0, emp_p, param_p)
    print(f"{col:<10} | {x0:<8.2f} | {emp_p:<10.4f} | {param_p:<10.4f}")

print("\nСгруппированные моменты:")
for col in cols:
    counts, bin_edges = np.histogram(df[col], bins='sturges')
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    mean_g = np.sum(counts * bin_centers) / n
    var_g = np.sum(counts * (bin_centers - mean_g) ** 2) / (n - 1)
    results_grouped[col] = (mean_g, var_g)
    print(f"{col}: Mean_g = {mean_g:.2f}, Var_g = {var_g:.2f}")

print("\nДоверительные интервалы (gamma=0.95):")
z = 1.96
for col in cols:
    std = df[col].std(ddof=1)
    mean = df[col].mean()
    err = z * (std / np.sqrt(n))
    print(f"{col} Дов. интервал: [{mean - err:.3f}, {mean + err:.3f}]")