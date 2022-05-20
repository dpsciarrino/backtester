from database import Database
import constants as consts
import utility as util
import backtest as bt
import pandas as pd
from orders import buy, short, _MARKET


class SMA(bt.Indicator):
    def __init__(self, name:str, *args, **kwargs):
        """
        SMA(name, period, series)
            name: str = Name of SMA indicator.
            period: int = Length of SMA
            series: pd.Series = Price series object.
        """

        # Instantiate the Indicator object __init__ method with the name of the indicator.
        super().__init__(name)

        # The parameters of an indicator must be passed as arguments.
        # In this case, args[0] is the 2nd argument and must be of type integer.
        if type(args[0]) != int:
            raise ValueError("Period must be int type.")
        
        # args[1] is the series object of prices, using the Pandas library as default
        if type(args[1]) != pd.Series:
            raise ValueError("Data must be of type pd.Series")

        # k = Length of the SMA indicator
        self._k = args[0]

        # series = The price series
        self._series = args[1]

    # This particular 'f' function returns a series of the same length as the original
    # _series passed into the Indicator object.
    def f(self) -> pd.Series:
        return pd.Series(self._series).rolling(self._k).mean()





class SimpleMovingAverage_Strategy(bt.Strategy):

    # This is used in the Backtest object to initialize your strategy.
    # Use this to define parameters and assign the indicators you want to base your strategy on.
    def init(self):
        # Name the strategy
        self._name = "SMA Crossover Strategy"

        # Add the indicators to your strategy.
        self.add_indicator(SMA("10-Period SMA", 10, self.data['close']))
        self.add_indicator(SMA("100-Period SMA", 100, self.data['close']))
    
    # Define your strategy here. Backtest runs this function to apply your strategy.
    def apply(self, current_data:pd.DataFrame, lookback_data:pd.DataFrame):
        above_10_period = float(current_data['close']) > current_data['10-Period SMA']

        sma10_above_sma100 = current_data['10-Period SMA'] > current_data['100-Period SMA']
        
        if( above_10_period and sma10_above_sma100):
            return buy(_MARKET, shares = 1, price=float(current_data['open']))
        elif ( sma10_above_sma100 == False):
            return short(_MARKET, shares = 1, price=float(current_data['close']))
        
        return None





# Creates the database object needed for backtesting
database = Database(db_name='stock_database.db')

# Specify parameters for dataframe construction
params = {
    'ticker': 'SPY',
    'timeframe': consts._DAY,
    'columns': ['datetime', 'close', 'open', 'high', 'low']
}
database.connect()
dataframe = database.get_dataframe(params=params)
database.disconnect()

# Instantiate the Strategy
strategy = SimpleMovingAverage_Strategy()

# Run the backtest using the dataframe and strategy objects
backtest = bt.Backtest(dataframe, strategy).run()