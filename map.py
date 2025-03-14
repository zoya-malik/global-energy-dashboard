import pandas as pd
import plotly.express as px

df = pd.read_csv("cleaned_primary_energy.csv")

df["Country"] = df["Country"].str.strip()

fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",  
    color="Total_Energy_Consumption_EJ",
    hover_name="Country",
    animation_frame="Year",  
    title="Global Energy Consumption Over Time",
    color_continuous_scale="Cividis", 
    range_color=[0, 200]
)

fig.show()

