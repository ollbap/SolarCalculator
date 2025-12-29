# Solar Predictor

A Python script that displays hourly solar irradiance forecasts for Las Rozas de Madrid, optimized for Termux terminal display on Android.

## Features

- **Hourly solar irradiance** (W/m²) for the next 5 days
- **Cloud coverage adjustment** using real-time forecasts from Open-Meteo API
- **Daily maximum reference** (clear-sky) for easy comparison
- **Compact table format** designed for mobile terminals
- **Zero external dependencies** - uses only Python standard library

## Output Example

```
Solar Irradiance - Las Rozas de Madrid
MAX (W/m²) = clear-sky reference | Values = % of MAX

       Mon 30  Tue 31  Wed 01  Thu 02  Fri 03
  MAX:    650     655     660     665     670
  ─────────────────────────────────────────────
  08:00     3%      7%      8%      4%      9%
  09:00    17%     32%     34%     18%     36%
  10:00    32%     61%     65%     33%     67%
  11:00    45%     86%     89%     45%     91%
  12:00    50%     96%    100%     50%    100%
  13:00    48%     92%     95%     48%     97%
  14:00    40%     76%     80%     41%     82%
  15:00    29%     57%     59%     30%     61%
  16:00    16%     31%     33%     17%     35%
  17:00    14%     25%     26%     12%     24%
```

- **MAX row**: Theoretical clear-sky maximum in W/m² (absolute reference)
- **Hourly values**: Percentage of MAX achieved after cloud adjustment

A value of 100% means clear sky at that hour. Lower percentages indicate cloud cover reducing solar irradiance.

## Quick Start

### Desktop (Linux/macOS)

```bash
# First time setup
chmod +x setup.sh run.sh
./setup.sh

# Run the predictor
./run.sh
```

### Termux (Android)

```bash
# First time setup
chmod +x setup_termux.sh run_termux.sh
./setup_termux.sh

# Run the predictor
./run_termux.sh
```

## Requirements

- Python 3.6+
- Internet connection (for cloud forecasts)

## Configuration

To change the location, edit these constants in `solar_predictor.py`:

```python
LATITUDE = 40.4930      # Your latitude
LONGITUDE = -3.8740     # Your longitude
LOCATION_NAME = "Las Rozas de Madrid"
```

To change the forecast period:

```python
FORECAST_DAYS = 5       # Number of days to show
```

## How It Works

1. **Sun position**: Uses NOAA Solar Calculator algorithms to compute solar elevation for each hour
2. **Clear-sky irradiance**: Calculates theoretical maximum using the Bird clear-sky model with air mass correction
3. **Cloud adjustment**: Fetches hourly cloud coverage from [Open-Meteo](https://open-meteo.com/) (free, no API key) and reduces irradiance accordingly
4. **Display**: Renders a compact table with hours as rows and days as columns

### Cloud Reduction Formula

```
actual_irradiance = clear_sky * (1 - cloud_cover% * 0.75)
```

- 0% clouds → 100% of clear-sky value
- 50% clouds → 62.5% of clear-sky value  
- 100% clouds → 25% of clear-sky value (diffuse radiation only)

## Data Source

Cloud coverage forecasts are provided by [Open-Meteo](https://open-meteo.com/), a free and open weather API that requires no API key.

## License

MIT License - Feel free to use and modify as needed.

