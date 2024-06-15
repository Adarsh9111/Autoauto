# autopilot
Generating cash on autopilot

Create a new virtual environment by executing

`python3 -m venv venv -r requirements.txt`

and then activate the environment with

`source venv/bin/activate`

### Fetching data from yahoo finance

To fetch data for a specific list of companies for a given period of time, pass it as a csv file in a format similar to faang.csv
and run the command:

`python3 --csv_uri=/path/to/file.csv 2023-01-01 2024-01-01` 

where the two dates are the start and end time to fetch data.

The output is always stored in the `data` folder.

If the csv_uri is missing from the arguments, automatically fetches the list of top 500 stocks in the US market and attempts to download historical data for the input 
time range