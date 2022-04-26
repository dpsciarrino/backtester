from database import Database
import constants as const
import pandas as pd

def get_dataframe_from_database(database:Database, ticker, timeframe=const._DAY, columns=[]) -> pd.DataFrame:
    params = {
        'ticker': ticker,
        'timeframe': timeframe,
        'columns': columns
    }
    database.connect()
    df = database.get_dataframe(params=params)
    database.close_connection()
    return df


def crossover(series1: pd.Series, series2: pd.Series):
    series1 = series1.values
    series2 = series2.values
    print(f"Comparing: {series1[-2]} and {series2[-2]}, {series1[-1]} and {series2[-1]}")
    return series1[-2] < series2[-2] and series1[-1] > series2[-1]