# Solar Incidence Calculator - Implementation Plan

## Overview

Build a Python script that calculates estimated solar irradiance (W/m²) for Las Rozas de Madrid (40.4930°N, 3.8740°W) using:
- **Astronomical calculations** for sun position and clear-sky irradiance
- **Open-Meteo API** for hourly cloud coverage forecasts (free, no API key)

Display a compact table with:
- **Header row**: MAX clear-sky irradiance in W/m² (theoretical maximum)
- **Data rows**: Percentage of MAX achieved (adjusted for clouds)
- **Columns**: Today + next 4 days (5 days total)

## Output Example

```
Solar Irradiance - Las Rozas de Madrid
MAX (W/m²) = clear-sky reference | Values = % of MAX

           Mon 30  Tue 31  Wed 01  Thu 02  Fri 03
  MAX:       650     655     660     665     670
  ─────────────────────────────────────────────
  08:00        3%      7%      8%      4%      9%
  09:00       17%     32%     34%     18%     36%
  10:00       32%     61%     65%     33%     67%
  11:00       45%     86%     89%     45%     91%
  12:00       50%     96%    100%     50%    100%
  13:00       48%     92%     95%     48%     97%
  14:00       40%     76%     80%     41%     82%
  15:00       29%     57%     59%     30%     61%
  16:00       16%     31%     33%     17%     35%
  17:00       14%     25%     26%     12%     24%
```

- **MAX row**: Clear-sky reference in W/m²
- **Hourly values**: Percentage of MAX (100% = clear, lower = clouds)

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

