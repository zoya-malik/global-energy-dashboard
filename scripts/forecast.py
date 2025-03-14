import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pmdarima import auto_arima

def load_energy_data():
    """
    Loads the dataset and ensures valid country selection.
    """
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/cleaned_primary_energy.csv"))
    df = pd.read_csv(file_path)
    df.rename(columns={"Year": "year", "Total_Energy_Consumption_EJ": "energy"}, inplace=True)
    return df

def get_available_countries():
    """
    Returns a list of available countries in the dataset.
    """
    df = load_energy_data()
    return sorted(df["Country"].unique())

def plot_forecast(country="United States", forecast_years=20):
    """
    Forecasts future energy consumption using pmdarima's auto_arima for better accuracy.
    """
    # 1. Load & Filter Data
    df = load_energy_data()
    if country not in df["Country"].unique():
        return "<p class='text-danger'>No data available for this country.</p>"

    df_country = df[df["Country"] == country].copy()
    if len(df_country) < 10:
        return "<p class='text-danger'>Not enough data to generate a reliable forecast.</p>"

    # 2. Sort by year and extract the series
    df_country.sort_values("year", inplace=True)
    years = df_country["year"].values
    series = df_country["energy"].values

    # 3. (Optional) Log transform if all values > 0
    log_transform = False
    if np.all(series > 0):
        log_transform = True
        series = np.log(series + 1e-9)  # add tiny offset to avoid log(0)

    # 4. Fit auto_arima to find best (p, d, q)
    try:
        model = auto_arima(
            series,
            start_p=0, start_q=0,
            max_p=5, max_q=5,
            seasonal=False,    # yearly data often not strongly seasonal
            trace=False,
            error_action="ignore",
            suppress_warnings=True,
            stepwise=True
        )
    except Exception as e:
        return f"<p class='text-danger'>auto_arima failed: {str(e)}</p>"

    # 5. Forecast
    try:
        forecast = model.predict(n_periods=forecast_years)
    except Exception as e:
        return f"<p class='text-danger'>Forecasting error: {str(e)}</p>"

    # 6. Invert log transform if applied
    if log_transform:
        series = np.exp(series)  # revert historical data
        forecast = np.exp(forecast)

    # 7. Build x-axis for forecast
    last_year = years[-1]
    forecast_years_list = np.arange(last_year + 1, last_year + forecast_years + 1)

    # 8. Plot with Plotly
    fig = go.Figure()

    # Historical
    fig.add_trace(go.Scatter(
        x=years,
        y=series,
        mode="lines+markers",
        name="Historical Energy Consumption",
        line=dict(color="blue")
    ))

    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast_years_list,
        y=forecast,
        mode="lines+markers",
        name="Forecasted Energy Consumption",
        line=dict(color="red", dash="dash")
    ))

    fig.update_layout(
        title=f"Energy Consumption Forecast for {country}",
        xaxis_title="Year",
        yaxis_title="Total Energy (EJ)",
        template="plotly_dark"
    )

    return fig.to_html(full_html=False)

