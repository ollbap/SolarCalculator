# Solar Incidence Calculator - Implementation Plan

## Overview

Build a Python script that calculates estimated solar irradiance (W/m²) for Las Rozas de Madrid (40.4930°N, 3.8740°W) using:
- **Astronomical calculations** for sun position and clear-sky irradiance
- **Open-Meteo API** for hourly cloud coverage forecasts (free, no API key)

Display a compact table with:
- **Header row**: MAX clear-sky irradiance for each day (theoretical maximum)
- **Data rows**: Cloud-adjusted irradiance by hour
- **Columns**: Today + next 4 days (5 days total)

## Output Example

```
Solar Irradiance (W/m²) - Las Rozas de Madrid
Cloud-adjusted values | MAX = clear-sky reference
           Mon 30  Tue 31  Wed 01  Thu 02  Fri 03
  MAX:       650     655     660     665     670
  ─────────────────────────────────────────────
  08:00       22      45      52      28      58
  09:00      108     210     225     115     235
  10:00      210     400     430     220     440
  11:00      290     560     590     300     600
  12:00      325     630     660     335     670
  13:00      310     600     630     320     640
  14:00      260     500     530     270     540
  15:00      190     370     390     200     400
  16:00      105     200     220     113     230
  17:00       90     165     170      83     160
```

## Technical Approach

### Open-Meteo API
- **Endpoint**: `https://api.open-meteo.com/v1/forecast`
- **Parameters**: latitude, longitude, hourly cloud_cover
- **Response**: Hourly cloud coverage percentage (0-100%)
- **No API key required**

### Solar Calculations
1. **Sun position**: NOAA Solar Calculator algorithms
2. **Clear-sky irradiance**: Bird model with air mass correction
3. **Cloud adjustment**: `actual = clear_sky * (1 - cloud_cover * 0.75)`
   - 0% clouds = 100% of clear-sky
   - 100% clouds = 25% of clear-sky (diffuse radiation)

## Files Created

| File | Purpose |
|------|---------|
| `solar_predictor.py` | Main script with all logic |
| `requirements.txt` | Python dependencies (none required) |
| `setup.sh` | Desktop setup: creates venv and installs deps |
| `setup_termux.sh` | Termux setup: installs Python and deps directly |
| `run.sh` | Desktop run script (activates venv and runs) |
| `run_termux.sh` | Termux run script |
| `README.md` | Project documentation |

## Dependencies
- **Python 3.6+**
- No external libraries required - pure Python implementation using standard `urllib`, `json`, `math`, and `datetime` modules

## Usage

**Desktop:**
```bash
./setup.sh      # First time only
./run.sh        # Run the predictor
```

**Termux:**
```bash
./setup_termux.sh   # First time only
./run_termux.sh     # Run the predictor
```

Note: Internet connection required to fetch cloud forecasts.

