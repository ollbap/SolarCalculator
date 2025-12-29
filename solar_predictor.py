#!/usr/bin/env python3
"""
Solar Irradiance Predictor for Las Rozas de Madrid
Displays hourly solar irradiance adjusted for cloud coverage forecasts.
Optimized for Termux terminal display.
"""

import math
import json
import ssl
from datetime import datetime, timedelta
from urllib.request import urlopen
from urllib.error import URLError

# Las Rozas de Madrid coordinates
LATITUDE = 40.4930
LONGITUDE = -3.8740
LOCATION_NAME = "Las Rozas de Madrid"

# Number of days to forecast
FORECAST_DAYS = 5

# Solar constant (W/m²)
SOLAR_CONSTANT = 1361


def get_julian_day(dt):
    """Calculate Julian Day from datetime."""
    a = (14 - dt.month) // 12
    y = dt.year + 4800 - a
    m = dt.month + 12 * a - 3
    jdn = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    return jdn + (dt.hour - 12) / 24 + dt.minute / 1440 + dt.second / 86400


def get_sun_position(dt, latitude, longitude):
    """
    Calculate sun elevation and azimuth using NOAA Solar Calculator algorithms.
    Returns (elevation_degrees, azimuth_degrees)
    """
    jd = get_julian_day(dt)
    jc = (jd - 2451545) / 36525  # Julian century
    
    # Geometric mean longitude of sun (degrees)
    geom_mean_long = (280.46646 + jc * (36000.76983 + 0.0003032 * jc)) % 360
    
    # Geometric mean anomaly of sun (degrees)
    geom_mean_anom = 357.52911 + jc * (35999.05029 - 0.0001537 * jc)
    
    # Eccentricity of Earth's orbit
    eccent = 0.016708634 - jc * (0.000042037 + 0.0000001267 * jc)
    
    # Sun equation of center
    sin_anom = math.sin(math.radians(geom_mean_anom))
    sin_2anom = math.sin(math.radians(2 * geom_mean_anom))
    sin_3anom = math.sin(math.radians(3 * geom_mean_anom))
    eq_of_center = sin_anom * (1.914602 - jc * (0.004817 + 0.000014 * jc)) + \
                   sin_2anom * (0.019993 - 0.000101 * jc) + sin_3anom * 0.000289
    
    # Sun true longitude and anomaly
    sun_true_long = geom_mean_long + eq_of_center
    
    # Sun apparent longitude
    omega = 125.04 - 1934.136 * jc
    sun_app_long = sun_true_long - 0.00569 - 0.00478 * math.sin(math.radians(omega))
    
    # Mean obliquity of ecliptic
    mean_obliq = 23 + (26 + (21.448 - jc * (46.815 + jc * (0.00059 - jc * 0.001813))) / 60) / 60
    
    # Corrected obliquity
    obliq_corr = mean_obliq + 0.00256 * math.cos(math.radians(omega))
    
    # Sun declination
    sun_declin = math.degrees(math.asin(math.sin(math.radians(obliq_corr)) * 
                                         math.sin(math.radians(sun_app_long))))
    
    # Equation of time (minutes)
    var_y = math.tan(math.radians(obliq_corr / 2)) ** 2
    eq_of_time = 4 * math.degrees(
        var_y * math.sin(2 * math.radians(geom_mean_long)) -
        2 * eccent * math.sin(math.radians(geom_mean_anom)) +
        4 * eccent * var_y * math.sin(math.radians(geom_mean_anom)) * math.cos(2 * math.radians(geom_mean_long)) -
        0.5 * var_y ** 2 * math.sin(4 * math.radians(geom_mean_long)) -
        1.25 * eccent ** 2 * math.sin(2 * math.radians(geom_mean_anom))
    )
    
    # True solar time
    time_offset = eq_of_time + 4 * longitude
    solar_time = dt.hour * 60 + dt.minute + dt.second / 60 + time_offset
    
    # Hour angle
    hour_angle = solar_time / 4 - 180
    if hour_angle < -180:
        hour_angle += 360
    
    # Solar zenith angle
    lat_rad = math.radians(latitude)
    declin_rad = math.radians(sun_declin)
    hour_rad = math.radians(hour_angle)
    
    cos_zenith = (math.sin(lat_rad) * math.sin(declin_rad) +
                  math.cos(lat_rad) * math.cos(declin_rad) * math.cos(hour_rad))
    cos_zenith = max(-1, min(1, cos_zenith))
    zenith = math.degrees(math.acos(cos_zenith))
    
    elevation = 90 - zenith
    
    # Solar azimuth
    if cos_zenith != 0:
        cos_azimuth = ((math.sin(lat_rad) * cos_zenith - math.sin(declin_rad)) /
                       (math.cos(lat_rad) * math.sin(math.radians(zenith))))
        cos_azimuth = max(-1, min(1, cos_azimuth))
        azimuth = math.degrees(math.acos(cos_azimuth))
        if hour_angle > 0:
            azimuth = 360 - azimuth
    else:
        azimuth = 180
    
    return elevation, azimuth


def get_sunrise_sunset(date, latitude, longitude):
    """
    Calculate sunrise and sunset times for a given date.
    Returns (sunrise_hour, sunset_hour) as floats.
    """
    jd = get_julian_day(datetime(date.year, date.month, date.day, 12, 0, 0))
    jc = (jd - 2451545) / 36525
    
    # Geometric mean longitude of sun
    geom_mean_long = (280.46646 + jc * (36000.76983 + 0.0003032 * jc)) % 360
    
    # Geometric mean anomaly of sun
    geom_mean_anom = 357.52911 + jc * (35999.05029 - 0.0001537 * jc)
    
    # Eccentricity of Earth's orbit
    eccent = 0.016708634 - jc * (0.000042037 + 0.0000001267 * jc)
    
    # Sun equation of center
    sin_anom = math.sin(math.radians(geom_mean_anom))
    sin_2anom = math.sin(math.radians(2 * geom_mean_anom))
    sin_3anom = math.sin(math.radians(3 * geom_mean_anom))
    eq_of_center = sin_anom * (1.914602 - jc * (0.004817 + 0.000014 * jc)) + \
                   sin_2anom * (0.019993 - 0.000101 * jc) + sin_3anom * 0.000289
    
    # Sun true longitude
    sun_true_long = geom_mean_long + eq_of_center
    
    # Sun apparent longitude
    omega = 125.04 - 1934.136 * jc
    sun_app_long = sun_true_long - 0.00569 - 0.00478 * math.sin(math.radians(omega))
    
    # Mean obliquity of ecliptic
    mean_obliq = 23 + (26 + (21.448 - jc * (46.815 + jc * (0.00059 - jc * 0.001813))) / 60) / 60
    obliq_corr = mean_obliq + 0.00256 * math.cos(math.radians(omega))
    
    # Sun declination
    sun_declin = math.degrees(math.asin(math.sin(math.radians(obliq_corr)) * 
                                         math.sin(math.radians(sun_app_long))))
    
    # Equation of time
    var_y = math.tan(math.radians(obliq_corr / 2)) ** 2
    eq_of_time = 4 * math.degrees(
        var_y * math.sin(2 * math.radians(geom_mean_long)) -
        2 * eccent * math.sin(math.radians(geom_mean_anom)) +
        4 * eccent * var_y * math.sin(math.radians(geom_mean_anom)) * math.cos(2 * math.radians(geom_mean_long)) -
        0.5 * var_y ** 2 * math.sin(4 * math.radians(geom_mean_long)) -
        1.25 * eccent ** 2 * math.sin(2 * math.radians(geom_mean_anom))
    )
    
    # Hour angle for sunrise/sunset
    lat_rad = math.radians(latitude)
    declin_rad = math.radians(sun_declin)
    
    cos_hour_angle = (math.cos(math.radians(90.833)) / (math.cos(lat_rad) * math.cos(declin_rad)) -
                      math.tan(lat_rad) * math.tan(declin_rad))
    
    if cos_hour_angle > 1:
        return None, None  # No sunrise (polar night)
    if cos_hour_angle < -1:
        return 0, 24  # No sunset (midnight sun)
    
    hour_angle = math.degrees(math.acos(cos_hour_angle))
    
    # Solar noon
    solar_noon = (720 - 4 * longitude - eq_of_time) / 60
    
    sunrise = solar_noon - hour_angle / 15
    sunset = solar_noon + hour_angle / 15
    
    return sunrise, sunset


def calculate_clear_sky_irradiance(elevation):
    """
    Calculate clear-sky Global Horizontal Irradiance (GHI) using simplified Bird model.
    Returns irradiance in W/m².
    """
    if elevation <= 0:
        return 0
    
    # Air mass calculation (Kasten-Young formula)
    zenith = 90 - elevation
    if zenith >= 90:
        return 0
    
    zenith_rad = math.radians(zenith)
    air_mass = 1 / (math.cos(zenith_rad) + 0.50572 * (96.07995 - zenith) ** -1.6364)
    
    # Simplified clear-sky model
    # Direct Normal Irradiance (DNI) with atmospheric attenuation
    tau = 0.7  # Atmospheric transmittance (typical clear day)
    dni = SOLAR_CONSTANT * (tau ** air_mass)
    
    # Global Horizontal Irradiance (GHI)
    ghi = dni * math.cos(zenith_rad)
    
    # Add diffuse component (approximately 10-15% of DNI for clear sky)
    diffuse = dni * 0.1 * math.sin(math.radians(elevation))
    
    return max(0, ghi + diffuse)


def fetch_cloud_forecast(latitude, longitude, days):
    """
    Fetch hourly cloud coverage forecast from Open-Meteo API.
    Returns dict with datetime string keys and cloud cover percentage values.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&hourly=cloud_cover"
        f"&forecast_days={days}"
        f"&timezone=auto"
    )
    
    try:
        # Create SSL context that doesn't verify certificates (for environments with SSL issues)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urlopen(url, timeout=10, context=ctx) as response:
            data = json.loads(response.read().decode())
            
        cloud_data = {}
        times = data["hourly"]["time"]
        clouds = data["hourly"]["cloud_cover"]
        
        for time_str, cloud in zip(times, clouds):
            cloud_data[time_str] = cloud if cloud is not None else 0
            
        return cloud_data
    except (URLError, KeyError, json.JSONDecodeError) as e:
        print(f"Warning: Could not fetch cloud data: {e}")
        print("Using clear-sky values only.\n")
        return {}


def apply_cloud_factor(clear_sky_irradiance, cloud_cover_percent):
    """
    Apply cloud reduction factor to clear-sky irradiance.
    Cloud cover of 100% reduces to ~25% (diffuse radiation only).
    """
    if cloud_cover_percent is None:
        return clear_sky_irradiance
    
    # Linear reduction with minimum 25% (diffuse component)
    reduction = 1 - (cloud_cover_percent / 100) * 0.75
    return clear_sky_irradiance * reduction


def format_table(data, dates, hours, max_values, clear_sky_totals, actual_totals):
    """
    Format the irradiance data as a compact table for terminal display.
    Shows MAX in W/m², daily totals, and hourly values as colored percentages.
    """
    # ANSI color codes
    RESET = "\033[0m"
    RED = "\033[91m"
    ORANGE = "\033[93m"
    YELLOW = "\033[33m"
    GREEN = "\033[92m"
    BRIGHT_GREEN = "\033[32m"
    DIM = "\033[2m"
    
    def colorize_pct(pct):
        """Apply color based on percentage value."""
        pct_str = f"{pct:>5}%"
        if pct >= 80:
            return f"{BRIGHT_GREEN}{pct_str}{RESET}"
        elif pct >= 60:
            return f"{GREEN}{pct_str}{RESET}"
        elif pct >= 40:
            return f"{YELLOW}{pct_str}{RESET}"
        elif pct >= 20:
            return f"{ORANGE}{pct_str}{RESET}"
        else:
            return f"{RED}{pct_str}{RESET}"
    
    lines = []
    
    # Title
    lines.append(f"Solar Irradiance - {LOCATION_NAME}")
    lines.append("")
    
    # Header with day names and dates
    header = "       "
    for date in dates:
        day_str = date.strftime("%a %d")
        header += f"  {day_str:>6}"
    lines.append(header)
    
    # Separator
    sep_width = 7 + len(dates) * 8
    lines.append("  " + "─" * (sep_width - 2))
    
    # Total daily irradiation row (Wh/m²)
    total_row = " TOTAL:"
    for date in dates:
        date_str = date.strftime("%Y-%m-%d")
        total_val = actual_totals.get(date_str, 0)
        total_row += f"  {int(total_val):>6}"
    lines.append(total_row)
    
    # Day efficiency row (actual vs clear-sky percentage)
    eff_row = "   EFF:"
    for date in dates:
        date_str = date.strftime("%Y-%m-%d")
        clear_total = clear_sky_totals.get(date_str, 0)
        actual_total = actual_totals.get(date_str, 0)
        if clear_total > 0:
            eff_pct = int(round(actual_total / clear_total * 100))
            eff_row += f"  {colorize_pct(eff_pct)}"
        else:
            eff_row += f"  {'--':>6}"
    lines.append(eff_row)
    
    # MAX row (clear-sky peak in W/m²)
    max_row = f"  {DIM} MAX:{RESET}"
    for date in dates:
        max_val = max_values.get(date.strftime("%Y-%m-%d"), 0)
        max_row += f"  {DIM}{int(max_val):>6}{RESET}"
    lines.append(max_row)
    
    # Separator
    lines.append("  " + "─" * (sep_width - 2))
    
    # Data rows (as colored percentage of daily MAX)
    for hour in hours:
        row = f"  {hour:02d}:00 "
        for date in dates:
            date_str = date.strftime("%Y-%m-%d")
            key = f"{date_str}T{hour:02d}:00"
            val = data.get(key)
            max_val = max_values.get(date_str, 0)
            
            if val is None or val <= 0 or max_val <= 0:
                row += f"  {DIM}{'--':>6}{RESET}"
            else:
                pct = int(round(val / max_val * 100))
                row += f"  {colorize_pct(pct)}"
        lines.append(row)
    
    # Legend
    lines.append("")
    lines.append(f"TOTAL: Daily irradiation (Wh/m²) | EFF: Day efficiency vs clear-sky")
    lines.append(f"MAX: Peak clear-sky (W/m²) | Colors: {BRIGHT_GREEN}≥80%{RESET} {GREEN}≥60%{RESET} {YELLOW}≥40%{RESET} {ORANGE}≥20%{RESET} {RED}<20%{RESET}")
    
    return "\n".join(lines)


def main():
    """Main entry point."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    dates = [today + timedelta(days=i) for i in range(FORECAST_DAYS)]
    
    # Determine hour range based on sunrise/sunset across all days
    min_sunrise = 24
    max_sunset = 0
    
    for date in dates:
        sunrise, sunset = get_sunrise_sunset(date, LATITUDE, LONGITUDE)
        if sunrise is not None:
            min_sunrise = min(min_sunrise, sunrise)
        if sunset is not None:
            max_sunset = max(max_sunset, sunset)
    
    # Round to full hours with padding
    start_hour = max(0, int(min_sunrise) - 1)
    end_hour = min(23, int(max_sunset) + 1)
    hours = list(range(start_hour, end_hour + 1))
    
    # Fetch cloud forecast
    print("Fetching cloud forecast from Open-Meteo...")
    cloud_data = fetch_cloud_forecast(LATITUDE, LONGITUDE, FORECAST_DAYS)
    
    # Calculate irradiance for each hour
    irradiance_data = {}
    max_values = {}
    clear_sky_totals = {}
    actual_totals = {}
    
    for date in dates:
        date_str = date.strftime("%Y-%m-%d")
        daily_max = 0
        daily_clear_sky_total = 0
        daily_actual_total = 0
        
        for hour in hours:
            dt = date.replace(hour=hour)
            elevation, _ = get_sun_position(dt, LATITUDE, LONGITUDE)
            
            # Calculate clear-sky irradiance
            clear_sky = calculate_clear_sky_irradiance(elevation)
            
            # Track daily maximum (clear-sky)
            if clear_sky > daily_max:
                daily_max = clear_sky
            
            # Add to daily clear-sky total
            daily_clear_sky_total += clear_sky
            
            # Apply cloud factor
            time_key = f"{date_str}T{hour:02d}:00"
            cloud_cover = cloud_data.get(time_key, 0)
            adjusted = apply_cloud_factor(clear_sky, cloud_cover)
            
            # Add to daily actual total
            daily_actual_total += adjusted
            
            irradiance_data[time_key] = adjusted
        
        max_values[date_str] = daily_max
        clear_sky_totals[date_str] = daily_clear_sky_total
        actual_totals[date_str] = daily_actual_total
    
    # Display table
    print()
    print(format_table(irradiance_data, dates, hours, max_values, clear_sky_totals, actual_totals))
    print()


if __name__ == "__main__":
    main()

