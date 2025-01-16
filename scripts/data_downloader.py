# script to help download datasets on a one-off basis
import pandas as pd
import requests
import os


# functions
def annual_runs_url_builder(url_year: int) -> str:
    """Creates the URL for cricinfo StatsGuru page for England test runs scored by year"""
    start_date = "spanmin2=01+Jan+" + str(url_year) + ";"
    end_date = "spanmax2=31+Dec+" + str(url_year) + ";"
    stats_url_prefix = "https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;orderby=runs;"
    stats_url_suffix = "spanval2=span;team=1;template=results;type=batting"
    stats_url = stats_url_prefix + start_date + end_date + stats_url_suffix
    return stats_url


def get_historical_top_scorer_table(top_scorer_year: int) -> pd.DataFrame:
    """Downloads the England top scorer table for the given year and saves in a DataFrame"""
    agent = {"User-Agent": "Mozilla/5.0"}
    top_scorers = pd.read_html(requests.get(annual_runs_url_builder(top_scorer_year), headers=agent).text)[2]
    keep_columns = ['Player', 'Mat', 'Inns', 'NO', 'Runs', 'HS', 'Ave', 'BF', 'SR', '100', '50', '0', '4s', '6s']
    return top_scorers[keep_columns].set_index('Player', drop=True)

if __name__ == "__main__":
    data_path = os.path.join("..", "data", "historical")
    selected_years = list(range(2012, 2025))
    saved_year_files = os.listdir(data_path)
    for year in selected_years:
        filename = "top_scorers_" + str(year) + ".csv"
        if not filename in saved_year_files:
            temp_top_scorers = get_historical_top_scorer_table(year)
            temp_top_scorers.to_csv(os.path.join(data_path, filename))
