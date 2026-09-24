import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('images', exist_ok=True)

# ==========================================
# Данные полупроводника
# ==========================================
T_semi = np.array([304,308,312,316,320,324,328,332,336,340,344,348,352,356,360,364,368,372,376])
I_semi = np.array([1302,1436,1592,1741,1878,1985,2138,2344,2509,2610,2660,2750,2820,2870,2920,2960,2950,3030,3060])
U_semi = np.array([1.237,1.132,1.011,0.899,0.789,0.702,0.621,0.544,0.5,0.472,0.419,0.376,0.33,0.294,0.26,0.233,0.208,0.184,0.165])

R_semi = U_semi / (I_semi * 1e-6)
ln_R = np.log(R_semi)

# Умножаем на 10^3 для удобного отображения на оси
inv_T_scaled = 1000 / T_semi

# Построение графика для полупроводника
plt.figure(figsize=(8, 6))
plt.plot(inv_T_scaled, ln_R, 'bo', label='Экспериментальные данные')
m, b = np.polyfit(inv_T_scaled, ln_R, 1)
plt.plot(inv_T_scaled, m * inv_T_scaled + b, 'r-', label='Аппроксимация')
plt.xlabel(r"$10^3/T$, $1/K$")
plt.ylabel(r"$\ln R$")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('images/plot_semi.png', dpi=300, bbox_inches='tight')
plt.close()


# ==========================================
# Данные металла
# ==========================================
T_metal = np.array([308,312,316,320,324,328,332,336,340,344,348,352,356,360,364,368,372,376])
I_metal = np.array([1175,1165,1153,1147,1137,1126,1116,1106,1096,1086,1075,1069,1062,1054,1046,1035,1032,1026])
U_metal = np.array([1.328,1.336,1.35,1.353,1.362,1.371,1.378,1.386,1.394,1.401,1.407,1.414,1.421,1.427,1.432,1.438,1.444,1.449])

R_metal = U_metal / (I_metal * 1e-6)
t_celsius = T_metal - 273.15

# Переводим Омы в килоомы для графика
R_metal_kOhm = R_metal / 1000

# Построение графика для металла
plt.figure(figsize=(8, 6))
plt.plot(t_celsius, R_metal_kOhm, 'ko', label='Экспериментальные данные')
m2, b2 = np.polyfit(t_celsius, R_metal_kOhm, 1)
plt.plot(t_celsius, m2 * t_celsius + b2, 'b-', label='Аппроксимация')
plt.xlabel(r"$t$, $^\circ C$")
plt.ylabel(r"$R$, кОм")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('images/plot_metal.png', dpi=300, bbox_inches='tight')
plt.close()

print("Графики успешно сохранены в папку 'images/'")