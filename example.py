from database import Database
import constants as consts
import utility as util
import backtest as bt
import pandas as pd
from orders import buy, short, _MARKET




# Retrieve the pricing data
db = Database(db_name='stock_database.db')
df = util.get_dataframe_from_database(db, 'SPY', consts._DAY, ['datetime', 'close', 'open', 'high', 'low'])

# Define a class extending the Indicator abstract class (found in the Backtest library)
class SMA(bt.Indicator):
    def __init__(self, name:str, *args, **kwargs):
        """
        SMA(name, period, series)
            name: str = Name of SMA indicator.
            period: int = Length of SMA
            series: pd.Series = Price series object.
        """
        super().__init__(name)

        if type(args[0]) != int:
            raise ValueError("Period must be int type.")
        if type(args[1]) != pd.Series:
            raise ValueError("Data must be of type pd.Series")

        self._k = args[0]
        self._series = args[1]

    def f(self) -> pd.Series:
        return pd.Series(self._series).rolling(self._k).mean()


class SimpleMovingAverage_Strategy(bt.Strategy):
    def init(self):
        self._name = "SMA Crossover Strategy"

        self.lookback = 1

        self.add_indicator(SMA("10-Period SMA", 10, self.data['close']))
        self.add_indicator(SMA("100-Period SMA", 100, self.data['close']))
    
    def apply(self, df:pd.DataFrame, prev_df:pd.DataFrame):
        above_10_period = float(df['close']) > df['10-Period SMA']
        above_100_period = float(df['close']) > df['100-Period SMA']

        sma10_above_sma100 = df['10-Period SMA'] > df['100-Period SMA']
        
        if( above_10_period and sma10_above_sma100):
            return buy(_MARKET, shares = 1, price=float(df['open']))
        elif ( sma10_above_sma100 == False):
            return short(_MARKET, shares = 1, price=float(df['close']))
        
        return None
        
    

s = SimpleMovingAverage_Strategy()

b = bt.Backtest(df, s).run()

