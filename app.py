from flask import Flask, render_template, request
from flask_cors import CORS

# Import from your scripts
from scripts.map import create_world_map
from scripts.forecast import plot_forecast, get_available_countries as get_forecast_countries
from scripts.leaderboard import (
    plot_leaderboard, get_available_years,
    plot_comparison, get_all_countries
)

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map')
def map_view():
    world_map_html = create_world_map()
    return render_template('map.html', world_map_html=world_map_html)

@app.route('/forecast')
def forecast():
    all_countries = get_forecast_countries()
    country = request.args.get("country")
    forecast_html = None
    if country:
        forecast_html = plot_forecast(country)
    return render_template(
        "forecast.html",
        all_countries=all_countries,
        forecast_html=forecast_html
    )

@app.route('/leaderboard', methods=["GET"])
def leaderboard():
    available_years = get_available_years()
    selected_year = request.args.get("year", default=available_years[-1], type=int)
    page = request.args.get("page", default=0, type=int)
    search_query = request.args.get("search", default="")
    leaderboard_html, total_pages = plot_leaderboard(selected_year, page, search_query)

    return render_template(
        "leaderboard.html",
        leaderboard_html=leaderboard_html,
        available_years=available_years,
        selected_year=selected_year,
        page=page,
        total_pages=total_pages,
        search_query=search_query
    )

@app.route('/compare', methods=["GET"])
def compare():
    country1 = request.args.get("country1")
    country2 = request.args.get("country2")
    all_countries = get_all_countries()
    comparison_html = None

    if country1 and country2:
        comparison_html = plot_comparison(country1, country2)

    return render_template(
        "comparison.html",
        comparison_html=comparison_html,
        all_countries=all_countries
    )

if __name__ == '__main__':
    print("🚀 Flask App Running on http://127.0.0.1:5000/")
    app.run(host="0.0.0.0", port=5000, debug=True)

