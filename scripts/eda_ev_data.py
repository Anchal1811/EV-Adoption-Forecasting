import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned data
data_path = os.path.join('..', 'outputs', 'cleaned_ev_population_data.csv')
df = pd.read_csv(data_path)
print("✅ Cleaned data loaded successfully!")
print("Shape:", df.shape)
print(df.head())

# --- EDA Section ---

# Basic info
print(df.info())
print(df.describe())

# Distribution of Model Year
plt.figure(figsize=(8,4))
sns.histplot(df['model_year'], bins=20, kde=True)
plt.title('Distribution of EV Model Year')
plt.xlabel('Model Year')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# Count of EVs by Make
plt.figure(figsize=(10,5))
top_makes = df['make'].value_counts().head(10)
sns.barplot(x=top_makes.index, y=top_makes.values)
plt.title('Top 10 EV Makes')
plt.xlabel('Make')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Average Electric Range by Make
avg_range = df.groupby('make')['electric_range'].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=avg_range.index, y=avg_range.values)
plt.title('Top 10 EV Brands by Average Electric Range')
plt.xlabel('Make')
plt.ylabel('Average Electric Range (miles)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# EV Type Distribution
plt.figure(figsize=(6,4))
sns.countplot(data=df, x='electric_vehicle_type')
plt.title('Distribution of EV Types')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

print("✅ EDA Completed Successfully!")
