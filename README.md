# autopilot
Generating cash on autopilot

Create a new virtual environment by executing

`python3 -m venv venv -r requirements.txt`

and then activate the environment with

`source venv/bin/activate`

### repository structure

- config: contains yaml files that define constants values that define system behavior
- framework: contains implementations of different operations that are necessary for creating and testing strategies
  - trading.py: contains framework code for creating and testing strategies
  - data.py: contains framework code for loading and processing data
- strategies: contains implementations of different strategies
- hdata: contains historical data for backtesting
- data: contains fresh data fetched periodically for calculating daily weight of stocks

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

#### infra 

- [ ] add date in the close/open index
- [ ] add tickers as a config [top 200]
- [x] setup backtesting data from 2017-2024 [freeze this, do not change]
- [x] update loader methods to fetch backtesting data by default but support custom files
- [x] create a new job to fetch data for all tickers for last 30 days (for calculating daily weights)
- [ ] pnl plot of cumulative return vector
- [ ] do not iterate over columns while processing values in mean reversion, use vectorization
- [ ] add sector neutralization
- [ ] add methods to validate the data files that are saved in backtesting / fresh data

#### trading

- [ ] explore APIs to trade
- [ ] how does shorting work
- [ ] fetch v-vap data
- [ ] sum, subtract, multiply, divide, power operators
- [ ] zscore, ts_rank, rank

### long term todos:

- [ ] compute draw down for strategies
- [ ] frontend
- [ ] printing library for backtest methods




#### Potential brokers

- interactive brokers
- gff brokers
- alpaca