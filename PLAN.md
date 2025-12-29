# Solar Incidence Calculator - Implementation Plan

## Overview

Build a Python script that calculates estimated solar irradiance (W/m²) for Las Rozas de Madrid (40.4930°N, 3.8740°W) using:
- **Astronomical calculations** for sun position and clear-sky irradiance
- **Open-Meteo API** for hourly cloud coverage forecasts (free, no API key)

Display a compact table with:
- **TOTAL row**: Daily irradiation in Wh/m²
- **EFF row**: Day efficiency (actual vs clear-sky percentage, colored)
- **MAX row**: Peak clear-sky irradiance in W/m²
- **Data rows**: Colored percentage of MAX at each hour
- **Columns**: Today + next 4 days (5 days total)

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
  ...
```

### Color Legend (in terminal)
- **Green (≥80%)**: Excellent solar conditions
- **Light Green (≥60%)**: Good conditions
- **Yellow (≥40%)**: Moderate conditions
- **Orange (≥20%)**: Poor conditions
- **Red (<20%)**: Very poor conditions

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

