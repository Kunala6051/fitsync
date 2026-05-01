import pandas as pd
import numpy as np

# Set a seed for reproducibility
np.random.seed(42)

# Generate dates
date_range = pd.date_range(start='2025-01-01', periods=365, freq='D')

# Generate synthetic data
steps = np.clip(np.random.normal(8500, 2500, len(date_range)), 3000, 18000)
sleep_hours = np.clip(np.random.normal(7.2, 1, len(date_range)), 4.5, 9.5)
heart_rate_bpm = np.clip(np.random.normal(68, 10, len(date_range)), 48, 110)
calories_burned = np.random.randint(1800, 4200, len(date_range))
active_minutes = np.random.randint(20, 180, len(date_range))

# Create DataFrame
data = pd.DataFrame({
    'Date': date_range,
    'Steps': steps,
    'Sleep_Hours': sleep_hours,
    'Heart_Rate_bpm': heart_rate_bpm,
    'Calories_Burned': calories_burned,
    'Active_Minutes': active_minutes
})

# Introduce 5 random NaNs in each column
for column in data.columns[1:]:  # Skip 'Date' column
    nan_indices = np.random.choice(data.index, size=5, replace=False)
    data.loc[nan_indices, column] = np.nan

# Save to CSV
data.to_csv('data/health_data.csv', index=False)
