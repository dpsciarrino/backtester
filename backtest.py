from abc import ABCMeta, abstractmethod
from typing import Type
import pandas as pd
from account import Account

class Indicator(metaclass=ABCMeta):
    def __init__(self, name:str):
        self._name = name
    
    @property
    def name(self):
        return self._name
    
    def __str__(self) -> str:
        return self._name
    
    def __repr__(self):
        return "<Indicator: " + self._name + ">"

    @abstractmethod
    def f(self):
        """
        Use this function to define the indicator series
        """
        pass

class Strategy(metaclass=ABCMeta):
    """
    Strategy Abstract Class
    """
    def __init__(self):
        self._name: str = ""
        self._data: pd.DataFrame = None
        self._indicators = {}
        self._lookback = 0
    
    @abstractmethod
    def init(self):
        pass
    
    @property
    def name(self):
        return self._name
    
    @property
    def data(self) -> pd.DataFrame:
        return self._data
    
    @data.setter
    def data(self, new_data:pd.DataFrame):
        self._data = new_data

    @property
    def indicators(self) -> list:
        """
        indicators

        Returns a list of the names of the assigned indicators.
        Indicator assignment is done by the user in the init() function of their strategy.
        """
        l = []
        for k, v in self._indicators.items():
            l.append(k)
        return l
    
    @property
    def lookback(self) -> int:
        """
        lookback

        Defines the number of previous (historical) data points to consider in the time series
        """
        return self._lookback
    
    @lookback.setter
    def lookback(self, k):
        """
        Sets the lookback value.

        This should be set by the user in their Strategy definition.
        """
        self._lookback = k

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return "<Strategy: " + self._name + ">"

    def add_indicator(self, i:Type[Indicator]):
        '''
        add_indicator

        Adds indicator 'i' to the indicator dictionary of the Strategy
        '''
        self._indicators[i.name] = i.f
    
    def run_indicator(self, name:str):
        '''
        run_indicator

        Runs the given indicator.
        '''
        return self._indicators[name]()



class Data:
    def __init__(self, data: pd.DataFrame):
        if data.empty:
            raise ValueError("Empty data passed to backtest.")
        self._data = data
        self._data_len = len(data)
    
    def add_column(self, name: str, column: pd.Series):
        self._data[name] = column
    
    def data(self, lookback:int=-1):
        '''
        data()

        Returns the data UP TO self._data_len
        lookback is set to a positive integer to view the previous 'lookback' rows up to self._data_len
        '''
        start:int = 0
        end:int = self._data_len
        if lookback < -1:
            raise ValueError("Lookback cannot be less than zero.")
        else:
            start = self._data_len - lookback

        return self._data.iloc[ start:end ]

    
    def _init(self):
        self._data_len = 0
    
    def _next(self):
        if self._data_len > len(self._data):
            raise IndexError("Last data row reached. Run _init to start over.")

        self._data_len += 1
        return self._data.iloc[self._data_len-1]
    
    def _has_next(self):
        return (self._data_len) < len(self._data)
        
    def __len__(self):
        return self._data_len


class Backtest:
    def __init__(self, data, strategy:Type[Strategy]):
        # Create Account object
        self._account = Account()

        # Create iterable data object containing dataframe
        self._data_test = Data(data)

        # Store Strategy for backtest to operate on
        self._strategy = strategy
        # Set the dataframe for the strategy
        self._strategy.data = data

        # Runs the USER-DEFINED init() function
        # This function is to be used to set up the Strategy
        # variables, extraneous sources, etc.
        self._strategy.init()
    
    def run(self):
        print(f"BACKTESTING STRATEGY: {self._strategy.name}...")

        # Each indicator has an 'f' function defined by the Indicator implementation
        # that defines how the Series is built. This cycles through each indicator, runs
        # it's 'f' function, and adds it to the dataframe as a column.
        for i in self._strategy.indicators:
            self._data_test.add_column(i, self._strategy.run_indicator(i))
            print(f"     INDICATOR ADDED: {i}")
        

        # Iterate through the data one at a time.
        self._data_test._init()
        while(self._data_test._has_next()):
            # Obtain the current data value
            current_data = self._data_test._next()

            # Obtain the 'lookback' number of past values for Strategy
            past_k_data = self._data_test.data(lookback = self._strategy.lookback)

            # Apply the strategy at this point in the data
            # obtain the Order type produced by the strategy
            order = self._strategy.apply(current_data, past_k_data)

            # Send order to brokerage account for processing
            order_amount = self._account.process_order(order)
            
            if order_amount != 0:
                print(order_amount)
        
        print(self._account.balance)
        