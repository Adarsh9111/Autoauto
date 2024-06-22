# autopilot
Generating cash on autopilot

Create a new virtual environment by executing

`python3 -m venv venv -r requirements.txt`

and then activate the environment with

`source venv/bin/activate`

### Fetching data from yahoo finance

To fetch data for a specific list of companies for a given period of time, pass it as a csv file in a format similar to faang.csv
and run the command from the autopilot folder:

`python3 scripts/fetch_historical_data.py --csv_uri=/path/to/file.csv 2023-01-01 2024-01-01` 

where the two dates are the start and end time to fetch data.

The output is always stored in the `data` folder.

If the csv_uri is missing from the arguments, automatically fetches the list of top 500 stocks in the US market and attempts to download historical data for the input 
time range

### Mean reversion strategy

To simulate the mean reversion strategy, ensure that the data is present in the /data folder.
Execute this command:

`python3 scripts/mean_reversion.py --lookback=5`

where the lookback can be changed to any value.

The output is the aggregated PnL in basis points achieved by trading over the entire set of stocks present in data

### todos

- [ ] add date in the close/open index
- [ ] schedule job to update latest data for each stock by appending to existing file
- [ ] add tickers as a config