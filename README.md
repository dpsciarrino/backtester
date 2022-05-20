# Backtester

Backtester is a framework for testing trading strategies.

This project is heavily influenced by the mechanics of the popular and fantastic Backtesting library on PyPI. The goal with this project, Backtester, is to harbor more versatility by allowing forms of data other than just pricing information into the Strategy and Indicator definitions.

## Setting Up the Database

### Disclaimer

This is the most important part. Due to the nature of the project, this needs to be followed to a T in order to have it work correctly IF YOU ARE TO START FROM SCRATCH.

However, the project itself relies on a Pandas dataframe. If you can build the dataframe in the expected format you should be able to use Backtester without issues. You will need to read this section to get a grasp of the expected format.

### Location

Currently, Backtester expects a SQLite database file to retrieve data. The default, expected database name is ```stock_database.db```. If you want to use a different name, you will need to change it using the ```db_name``` parameter when instantiating the Database object (see later section on Usage).

Create a folder called ```data``` that sits in the parent directory of the project, like so:

Parent_Directory
  - backtester
    - README.md
    - backtest.py
    - ...
  - data
    - stock_database.db

### Table Names

The tables in the database need to have the following naming convention:
    ```<Ticker>_<Number_Of_Intervals><Interval_Type>```

Where:
- ```<Ticker>``` is the ticker of the stock/security
- ```<Interval_Type>``` is the timeframe interval. It can be either:
    - 'Min'
    - 'Day'
- ```<Number_Of_Intervals>``` is the number of timeframe intervals between each row in the data.

For example, ```BA_1Day``` means you have data from ticker BA and the timeframe between each row is 1 Day. Similarly, ```MMM_1Min``` means you have data from ticker MMM and the timeframe between each row is 1Min.

### Table Structure

The table structure for Daily data is as follows:

```| datetime | open | high | low | close | volume |```

All fields are TEXT. The ```datetime``` is setup as a primary key and should be in ```YYYY-MM-DD``` format.

The table structure for Minute data is the same as above, with the exception that ```datetime``` should be in ```YYYY-MM-DD HH:MM``` format.

I recommend generating a CSV file, cleaning that up, and migrating that to a SQLite database, following the naming and format guidelines above.

### Using the Database

To use the database, instantiate a Database object using the following line:

```
from database import Database

database = Database(db_name='stock_database.db')
```

where the assignment to ```db_name``` is the SQLite database filename.

If you have another path other than the parent directory of this project you can specify it using the ```db_path``` parameter:

```
from pathlib import Path as p

# Create the path to the parent directory of the SQLite file using the Path object
my_db_path = .../path/to/my/database/file

database = Database(db_name='stock_database.db', dp_path=my_db_path)
```

Opening the database:
``` database.connect() ```

Closing the database:
``` database.disconnect() ```

### Creating the Dataframe

Converting the database data into a dataframe object can be done in the following way:

First, specify the ticker and timeframe you want to use (make sure the corresponding table is in your database). Also, specify the columns you want included in the dataframe via a list of strings.
```
params = {
    'ticker': 'SPY',
    'timeframe': 'DAY',
    'columns': ['datetime', 'close', 'open', 'high', 'low']
}
```

Then, connect to the database. The Database object has a function called ``` get_dataframe(params=...) ``` which creates a dataframe from the specified parameters. Finally close the database.
```
database.connect()
dataframe = database.get_dataframe(params=params)
database.disconnect()
```

You now have a database you can use for backtesting, along with any other desired operations.

## Creating Indicators

Indicators are defined with at least the following functions:
- `__init__`: ```__init__(self, name:str, *args, **kwargs)```
- f: ```f(self) -> pd.Series```

### Initializing an Indicator

Indicators are classes that extend the Indicator class in the backtest.py file. The ```__init__``` of the custom indicator should have ```name``` as the first argument.

Additional parameters used for the indicator (such as period or a series to act on) should be passed in using the typical args and kwargs, which the user must define and use to their own dicretion.

Always call ```super().__init__(name)``` when initializing the custom Indicator object.

It's a good idea to error check the parameters you pass into ```args``` and raise the correct Exceptions.

To use the parameters, register then as instance variables using ```self```.

### The 'f' Function

The 'f' function is used to run your indicator during the backtest. It should return a pandas Series object, ideally the same length (number of rows) as the pricing data you are backtesting over.

### Indicator Example

The ```example.py``` file has an example of a Simple Moving Average Indicator.

## Creating Strategies

The Strategy object requires two functions to be defined:
- init: ```init(self)```
- apply: ```apply(self, current_data:pd.Dataframe, lookback_data:pd.Dataframe)```

### Initializing a Strategy

Strategies are classes that extend the Strategy class found in the ```backtest.py``` file.

Notice that the ```init()``` function required for the strategy definition is not the magic method. Also, no calls to super() are needed in this instance.

Use the ```init()``` method to specify a name using ```self._name = "..."```.

Also, add any indicators you need to define your strategy using the ```add_indicator(i)``` method provided by the extended Strategy class, where `i` is an instance of the Indicator you defined above.

### The apply() Function

The apply function is used by the Backtest to implement your strategy on each row of data in an iterated fashion. It should have the following structure:

```
def apply(self, current_data:pd.Dataframe, lookback_data:pd.DataFrame):
    ...
```

The ```current_data``` parameter represents the current row of pricing data during the iteration of the backtest.

The ```lookback_data``` parameter represents the current row, along with the previous ```lookback``` rows of pricing data and is served as a Dataframe object. The integer ```lookback``` setting can be set during the Strategy initialization (in the ```init``` function) using ```self.lookback = ... ```.

The lookback feature is put in place because sometimes you have strategies that require historical pricing information. This is provided as a mechanism you can use to access past data during the backtest iteration.

### Strategy Example

The ```example.py``` file has an example of a Simple Moving Average Strategy.

## Backtesting

The backtesting function (the whole point of this project!!) is still being developed...

### Running a Backtest

Currently, if you followed what's outlined in the README above, you can run a backtest using the following block:

```
from database import Database
import backtest

database = Database(db_name='stock_database.db')
params = {
    'ticker': 'SPY',
    'timeframe': 'DAY',
    'columns': ['datetime', 'close', 'open', 'high', 'low']
}
database.connect()
dataframe = database.get_dataframe(params=params)
database.disconnect()
strategy = Your_Strategy()
backtest.Backtest(dataframe, strategy).run()
```

Where you must define ```Your_Strategy()``` as exemplified in the ```example.py``` file.

Again, this is currently under development and will probably spit out a bunch of results that aren't readily useful at this point. Stay tuned, though. Exciting things are coming.