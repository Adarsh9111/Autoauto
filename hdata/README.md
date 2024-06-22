### hdata

hdata contains all the historical data for the universe of stocks in the given time range in config.

**This data should never be modified and should only be used in a read-only mode.**

If for whatever reason the data needs to be refreshed, follow the steps given below.

1. From `autopilot` folder, run the following command:

```
python3 framework/refresh_historical_data.py 
```

This assumes that the autopilot folder has a `config.yaml` file present. If the file is present elsewhere
pass the location of file using 

```
python3 framework/refresh_historical_data.py --config_path=/path/to/config/yaml
```

2. The data should be automatically downloaded and saved in the `hdata` folder


