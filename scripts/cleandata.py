import pandas as pd

df_primary = pd.read_csv("Primary energy consumption - EJ.csv")
df_fuel = pd.read_csv("Energy_consumption_by_fuel_EJ.csv")

df_primary = df_primary.dropna(axis=1, how='all')
df_fuel = df_fuel.dropna(axis=1, how='all')

df_primary["Country"] = df_primary["Country"].str.strip()
df_fuel["Country"] = df_fuel["Country"].str.strip()

country_map = {
    "Russian Federation": "Russia",
    "USSR": "Russia",
    "United States": "USA",
    "United Kingdom": "UK",
    "South Korea": "Korea, Rep.",
    "Czech Republic": "Czechia",  # Fix Czech Republic name
    "Taiwan": "Taiwan, Province of China"  # Fix Taiwan mapping
}
df_primary["Country"] = df_primary["Country"].replace(country_map)
df_fuel["Country"] = df_fuel["Country"].replace(country_map)

df_primary = df_primary.groupby(["Country", "Year"], as_index=False).sum()

print("Missing values in Primary Energy Dataset:")
print(df_primary.isnull().sum())

print("\nMissing values in Fuel Energy Dataset:")
print(df_fuel.isnull().sum())

df_primary = df_primary.fillna(0)
df_fuel = df_fuel.fillna(0)

df_primary.to_csv("cleaned_primary_energy.csv", index=False)
df_fuel.to_csv("cleaned_fuel_energy.csv", index=False)

print("Data cleaning complete! Cleaned files saved as 'cleaned_primary_energy.csv' and 'cleaned_fuel_energy.csv'.")

