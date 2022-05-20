# Backtester

Backtester is a framework for testing trading strategies.

## Setting Up the Database

### Location

Currently, Backtester expects a SQLite database file to retrieve data. The default, expected database name is 'stock_database.db'. If you want to use a different name, you will need to change it using the db_name parameter when instantiating the Database object (see later section on Usage).

Create a folder called 'data' that sits in the parent directory of the project, like so:

Parent_Directory
  - backtester
    - README.md
    - backtest.py
    - ...
  - data
    - stock_database.db

### Table Names

The tables in the database need to have the following naming convention:
    <Ticker>_<Number_Of_Intervals><Interval_Type>

Where:
- <TICKER> is the ticker of the stock/security
- <Interval_Type> is the timeframe interval. It can be either:
    - 'Min'
    - 'Day'
- <Number_Of_Intervals> is the number of timeframe intervals between each row in the data.

For example, BA_1Day means you have data from ticker BA and the timeframe between each row is 1 Day. Similarly, MMM_1Min means you have data from ticker MMM and the timeframe between each row is 1Min.

### Table Structure

The table structure for Daily data is as follows:
  | datetime | open | high | low | close | volume |

All fields are TEXT. The 'datetime' is setup as a primary key and should be in 'YYYY-MM-DD' format.

The table structure for Minute data is the same as above, with the exception that datetime should be in 'YYYY-MM-DD HH:MM' format.

I recommend generating a CSV file, cleaning that up, and migrating that to a SQLite database, following the naming and format guidelines above.

### Using the Database

To use the database, instantiate a Database object using the following line:

```database = Database(db_name='stock_database.db')```

where the assignment to db_name is the SQLite database filename.

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

