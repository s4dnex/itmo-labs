from src.main import compute_cn

R = 421.0
T = 1.0
N_check = 10

# --- Равенство Парсеваля ---

# Аналитическая формула
energy_LHS = (4 / 3) * (R ** 2)

# Сумма ряда
energy_RHS = 0

for n in range(-N_check, N_check + 1):
    mag_sq = abs(compute_cn(n)) ** 2
    energy_RHS += mag_sq

print("-" * 50)
print(f"Теоретическое значение: {energy_LHS:.2f}")
print(f"Частичная сумма ряда при N = {N_check}: {energy_RHS:.2f}")
print(f"Разница: {energy_LHS - energy_RHS:.2f} ({((energy_RHS - energy_LHS) / energy_LHS) * 100:.4f}%)")