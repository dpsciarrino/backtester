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
    database.disconnect()
    return df
