import pandas as pd
import numpy as np
import os

# Define paths
input_path = os.path.join('..', 'data', 'Electric_Vehicle_Population_Data.csv')
output_path = os.path.join('..', 'outputs', 'cleaned_ev_population_data.csv')

# Load data
df = pd.read_csv(input_path)
print("✅ Raw data loaded successfully!")
print("Shape:", df.shape)
print(df.head())

# ---- Handle missing values ----
df['Electric Range'] = df['Electric Range'].fillna(df['Electric Range'].median())
df['Model Year'] = df['Model Year'].fillna(df['Model Year'].mode()[0])
df['Make'] = df['Make'].fillna('Unknown')
df['Model'] = df['Model'].fillna('Unknown')

# Drop rows with too many missing values
df = df.dropna(thresh=len(df.columns) - 3)

# ---- Clean column names ----
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# ---- Convert categorical variables ----
cat_cols = ['make', 'model', 'county', 'electric_vehicle_type']
for col in cat_cols:
    if col in df.columns:
        df[col] = df[col].astype('category')
        df[col + '_code'] = df[col].cat.codes

# ---- Remove duplicates ----
print("Duplicates before:", df.duplicated().sum())
df = df.drop_duplicates()
print("Duplicates after:", df.duplicated().sum())

# ---- Feature engineering ----
df['is_bev'] = df['electric_vehicle_type'].apply(lambda x: 1 if 'Battery Electric' in str(x) else 0)
df['is_phev'] = df['electric_vehicle_type'].apply(lambda x: 1 if 'Plug-in Hybrid' in str(x) else 0)
df['county'] = df['county'].astype(str).str.title()

# Average electric range by make
avg_range_per_make = df.groupby('make')['electric_range'].mean().reset_index()
avg_range_per_make.columns = ['make', 'avg_electric_range']
df = df.merge(avg_range_per_make, on='make', how='left')

# ---- Clean model year ----
df['model_year'] = pd.to_numeric(df['model_year'], errors='coerce')
df = df[(df['model_year'] >= 2000) & (df['model_year'] <= 2025)]

# ---- Save cleaned dataset ----
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)
print(f"✅ Cleaned dataset saved to: {output_path}")
print("Final Shape:", df.shape)
