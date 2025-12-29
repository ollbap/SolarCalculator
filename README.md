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

         Mon 30  Tue 31  Wed 01  Thu 02  Fri 03
  ─────────────────────────────────────────────
 TOTAL:    1328     992     732     356     890
   EFF:     95%     71%     52%     25%     64%
   MAX:     296     297     298     300     305
  ─────────────────────────────────────────────
  08:00      0%      0%      0%      0%      0%
  09:00     11%     12%      7%      4%      8%
  10:00     37%     35%     18%     13%     28%
  11:00     85%     55%     38%     21%     52%
  12:00    100%     66%     56%     25%     72%
  13:00     96%     73%     65%     24%     68%
  14:00     74%     60%     42%     19%     55%
  15:00     39%     29%     18%     10%     32%
  16:00      6%      4%      2%      2%      5%
```

### Reading the Output

- **TOTAL**: Daily irradiation in Wh/m² (sum of all hourly values)
- **EFF**: Day efficiency - percentage of clear-sky potential achieved (colored)
- **MAX**: Peak clear-sky irradiance in W/m² (reference value)
- **Hourly values**: Percentage of MAX at each hour (colored)

### Color Legend (in terminal)

| Color | Range | Meaning |
|-------|-------|---------|
| Green | ≥80% | Excellent solar conditions |
| Light Green | ≥60% | Good conditions |
| Yellow | ≥40% | Moderate conditions |
| Orange | ≥20% | Poor conditions |
| Red | <20% | Very poor conditions |

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

Edit `config.py` to customize the predictor:

```python
# Location coordinates
LATITUDE = 40.4930
LONGITUDE = -3.8740
LOCATION_NAME = "Las Rozas de Madrid"

# Number of days to forecast (1-16, Open-Meteo supports up to 16 days)
FORECAST_DAYS = 7
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

