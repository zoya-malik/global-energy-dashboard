import os
import pandas as pd
import plotly.express as px

def load_energy_data():
    """Loads the primary energy dataset."""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/cleaned_primary_energy.csv"))
    df = pd.read_csv(file_path)
    df.rename(columns={"Year": "year", "Total_Energy_Consumption_EJ": "energy"}, inplace=True)
    return df

def get_available_years():
    """Returns available years for the leaderboard."""
    df_energy = load_energy_data()
    return sorted(df_energy["year"].unique())

def get_all_countries():
    """Returns a list of all available countries."""
    df_energy = load_energy_data()
    return sorted(df_energy["Country"].unique())

def plot_leaderboard(selected_year, page=0, search_query="", page_size=7):
    """Creates a paginated leaderboard with search and improved visuals."""
    df = load_energy_data()
    df = df[df["year"] == selected_year]

    if search_query:
        df = df[df["Country"].str.contains(search_query, case=False, na=False)]

    df = df.sort_values(by="energy", ascending=True)

    max_energy = df["energy"].max()
    total_pages = (len(df) // page_size) + 1
    df_paginated = df.iloc[page * page_size : (page + 1) * page_size]

    bar_width = 0.2 if len(df_paginated) == 1 else 1

    fig = px.bar(
        df_paginated, x="energy", y="Country",
        orientation="h",
        title=f"Energy Consumption Ranking ({selected_year})",
        labels={"energy": "Total Energy (EJ)"},
        color="energy",
        color_continuous_scale="viridis"
    )

    fig.update_traces(marker=dict(line=dict(color="black", width=2)), width=bar_width)

    return fig.to_html(full_html=False), total_pages

def plot_comparison(country1, country2):
    """Compares two countries' energy consumption over time."""
    df = load_energy_data()
    df = df[df["Country"].isin([country1, country2])]

    fig = px.line(
        df, x="year", y="energy", color="Country",
        title=f"Energy Consumption: {country1} vs {country2}",
        labels={"energy": "Total Energy (EJ)"}
    )

    # Log scale to handle big differences
    fig.update_yaxes(type="log", title_text="Total Energy (EJ, Log Scale)")

    return fig.to_html(full_html=False)

