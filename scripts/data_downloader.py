# script to help download datasets on a one-off basis
import pandas as pd
import requests
import os
import datetime
from io import StringIO

# functions
def runs_between_dates_url_builder(start_date: datetime.date, end_date: datetime.date) -> str:
    """Creates the URL for cricinfo StatsGuru page for England test runs scored during a given time period
     Includes matches starting between start_date and end_date inclusive"""
    target_format = "%d+%b+%Y"
    start_date_text = "spanmin2=" + start_date.strftime(target_format) + ";"
    end_date_text = "spanmax2=" + end_date.strftime(target_format) + ";"
    stats_url_prefix = "https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;orderby=runs;"
    stats_url_suffix = "spanval2=span;team=1;template=results;type=batting"
    stats_url = stats_url_prefix + start_date_text + end_date_text + stats_url_suffix
    return stats_url

def get_top_scorer_table(start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    """Downloads the England top scorer table for the given time period and returns as a DataFrame"""
    agent = {"User-Agent": "Mozilla/5.0"}
    page_tables = pd.read_html(StringIO(requests.get(runs_between_dates_url_builder(start_date, end_date),
                                                     headers=agent).text))
    # if there is no data (yet) for that top_scorer_year, then the page table(s) are not generated
    if len(page_tables) < 8:
        return pd.DataFrame()
    top_scorers = page_tables[2]
    keep_columns = ['Player', 'Mat', 'Inns', 'NO', 'Runs', 'HS', 'Ave', 'BF', 'SR', '100', '50', '0', '4s', '6s']
    return top_scorers[keep_columns].set_index('Player', drop=True)

def get_historical_annual_top_scorer_table(top_scorer_year: int) -> pd.DataFrame:
    """Downloads the England top scorer table for the given year and returns as a DataFrame"""
    start_date = datetime.date(top_scorer_year,1,1)
    end_date = datetime.date(top_scorer_year, 12, 31)
    return get_top_scorer_table(start_date, end_date)

if __name__ == "__main__":
    data_path = os.path.join("..", "data", "historical")
    selected_years = list(range(2012, 2025))
    saved_year_files = os.listdir(data_path)
    for year in selected_years:
        filename = "top_scorers_" + str(year) + ".csv"
        if not filename in saved_year_files:
            temp_top_scorers = get_historical_annual_top_scorer_table(year)
            temp_top_scorers.to_csv(os.path.join(data_path, filename))
