import pandas as pd
import numpy as np

np.random.seed(42)
n_days = 5000

# Дни с последнего полива
days_since_last_water = np.zeros(n_days, dtype=int)
for i in range(1, n_days):
    if np.random.rand() < 0.12:
        days_since_last_water[i] = 0
    else:
        days_since_last_water[i] = days_since_last_water[i-1] + 1

days = np.arange(n_days)

# Температура и ET0
temp_avg = 10 + 15 * np.sin(2 * np.pi * days / 365) + np.random.normal(0, 3, n_days)
temp_avg = np.clip(temp_avg, 5, 38)

et0 = np.clip(2 + 5 * np.sin(2 * np.pi * days / 365) + np.random.normal(0, 1.5, n_days), 1, 9)

# Осадки
precip_daily = np.random.exponential(1.2, n_days) * (np.random.rand(n_days) < 0.15)
precip_7d = pd.Series(precip_daily).rolling(7, min_periods=1).sum().values

# Влажность почвы
soil_moisture = np.zeros(n_days)
soil_moisture[0] = 0.25
for i in range(1, n_days):
    soil_moisture[i] = soil_moisture[i-1] * 0.92 - 0.01 * et0[i] + 0.8 * precip_daily[i]
    soil_moisture[i] = np.clip(soil_moisture[i], 0.05, 0.45)

# Дни с посева
days_since = np.zeros(n_days, dtype=int)
for i in range(1, n_days):
    if np.random.rand() < 0.12:
        days_since[i] = 0
    else:
        days_since[i] = days_since[i-1] + 1

# Культура
crop = np.random.choice([0, 1], n_days, p=[0.55, 0.45])

# Коэффициент культуры (kc)
kc_base = np.where(crop == 0,  # кукуруза
    0.30 + 0.9 * np.minimum(days_since / 45, 1),
    0.35 + 0.8 * np.minimum(days_since / 35, 1))  # пшеница
kc = np.clip(kc_base, 0.3, 1.2)

etc = et0 * kc

# вычит полива
irrigation_mm = np.maximum(0, etc - precip_7d * 0.75 - soil_moisture * 25 + days_since * 0.5 + days_since_last_water * 0.3)
irrigation_mm += np.random.normal(0, 1.2, n_days)
irrigation_mm = np.clip(irrigation_mm, 0, 18)

df = pd.DataFrame({
    "temp_avg": temp_avg,
    "et0": et0,
    "precip_7d": precip_7d,
    "wind": np.random.uniform(1, 8, n_days),
    "soil_moisture": soil_moisture,
    "days_since": days_since,
    "days_since_last_water": days_since_last_water,
    "crop": crop,
    "irrigation_mm": irrigation_mm
})

df["phase_progress"] = np.clip(
    (df["days_since"] / 45.0) + (df["temp_avg"] / 100.0) - (df["irrigation_mm"] / 50.0) + np.random.normal(0, 0.08, n_days),
    0.0, 1.0
)

df.to_csv("irrigation_data_improved.csv", index=False)
print("данные созданы")
print("Размер датасета:", df.shape)
print("Колонки:", df.columns.tolist())
print("\nПервые 3 строки:\n", df.head(3))