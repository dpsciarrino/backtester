import sqlite3
from argparse import ArgumentError
import pandas as pd
import constants as consts

def generate_query_select_string(ticker:str, timeframe:str=consts._DAY, columns:list=[]):
    """
    ticker: Ticker of the stock.
    timeframe: 'Min' for minute data, 'Day' for daily data. Default = 'Day'.
    columns: Specify the column names you wish to extract. Default = [] for all columns.
    """
    if timeframe.upper() != consts._DAY and timeframe.upper() != consts._MIN:
        raise ArgumentError(None, "timeframe should be 'MIN' or 'DAY'")

    query = ""
    if len(columns)>0:
        col_str = ""
        for column in columns:
            col_str += (column + ", ")

        col_str = col_str[:len(col_str)-2]
        query = f"""SELECT {col_str} FROM {ticker}_1{timeframe.upper()}"""

        return query

    return f"""SELECT * FROM {ticker}_1{timeframe.upper()}"""



class Database:
    def __init__(self, db_name='stock_database.db', db_path=consts._DATABASE_PATH):
        self._name = db_name
        self._path = db_path / db_name
        self._conn = None
        self._internalCursor = None
        self._cursors = {}
    
    @property
    def is_connected(self):
        return self._conn != None

    @property
    def cursor_list(self):
        cursors = []
        for key, val in self._cursors.items():
            cursors.append(key)
        return cursors
    
    def path(self):
        return self._path
    
    def connect(self):
        try:
            self._conn = sqlite3.connect(self._path)
            self._internalCursor = self._conn.cursor()
        except Exception as e:
            print(e.args)
    
    def get_connection(self):
        return self._conn
    
    def generate_cursor(self, cursor_name: str):
        self._cursors[cursor_name] = self._conn.cursor()
        return self._cursors[cursor_name]
    
    def get_cursor_by_name(self, name):
        return self._cursors[name]
    
    def disconnect(self):
        if self._conn != None:
            self._conn.close()
            self._conn = None
            return 0
        return -1
    
    def run_select_query(self, query):
        self._internalCursor.execute(query)
        return self._internalCursor.fetchall()
    
    def get_dataframe(self, params={}, ticker="", timeframe=consts._DAY, columns=[]):
        if self._conn == None:
            raise Exception(message="Connect to database before performing this action.")
        
        if len(params) > 0:
            ticker = params['ticker']
            timeframe = params['timeframe']
            columns = params['columns']

        query = generate_query_select_string(ticker, timeframe, columns)
        df = pd.read_sql_query(query, self._conn)

        return df
    



