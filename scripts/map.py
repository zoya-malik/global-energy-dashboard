import os
import pandas as pd
import plotly.express as px

def create_world_map():
    """
    Loads the cleaned energy data and creates an interactive world map with animation.
    """
    file_path = os.path.abspath("data/cleaned_primary_energy.csv")
    df = pd.read_csv(file_path)

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

    return fig.to_html(full_html=False)

