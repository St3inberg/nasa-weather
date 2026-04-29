#!/usr/bin/env python3
"""
NASA Mars Weather Fetcher for Home Assistant
Fetches data from NASA's InSight Mars Weather Service
"""

import requests
import json
import os
from datetime import datetime
import sys

BASE_URL = "https://api.nasa.gov/insight_weather/"


def _normalize(data: dict) -> dict | None:
    """Normalize both legacy (av_t/av_p/av_ws) and sol-key (AT/PRE/HWS) API formats."""
    if not isinstance(data, dict):
        return None

    if "av_t" in data or "av_p" in data or "av_ws" in data:
        return data

    sol_keys = data.get("sol_keys")
    if not isinstance(sol_keys, list) or not sol_keys:
        return None

    latest_sol = sorted(
        sol_keys,
        key=lambda s: (0, int(s)) if str(s).isdigit() else (1, str(s)),
    )[-1]
    sol = data.get(latest_sol)
    if not isinstance(sol, dict):
        return None

    return {
        "av_t": sol.get("AT") or sol.get("av_t") or {},
        "av_p": sol.get("PRE") or sol.get("av_p") or {},
        "av_ws": sol.get("HWS") or sol.get("av_ws") or {},
        "wd": sol.get("WD") or sol.get("wd") or {},
        "source_sol": latest_sol,
    }


def fetch_mars_weather():
    """Fetch latest Mars weather data from NASA API"""
    api_key = os.environ.get("NASA_API_KEY")

    if not api_key:
        print("Error: NASA_API_KEY environment variable not set", file=sys.stderr)
        return None

    params = {"feedtype": "json", "ver": "1.0", "api_key": api_key}

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return _normalize(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return None


def parse_weather_data(data):
    """Parse and format weather data"""
    if not data or "av_t" not in data:
        return None

    weather = {
        "timestamp": datetime.now().isoformat(),
        "sol": data.get("source_sol"),
        "temperature": {
            "average": data.get("av_t", {}).get("av"),
            "min": data.get("av_t", {}).get("mn"),
            "max": data.get("av_t", {}).get("mx"),
        },
        "pressure": {
            "average": data.get("av_p", {}).get("av"),
            "min": data.get("av_p", {}).get("mn"),
            "max": data.get("av_p", {}).get("mx"),
        },
        "wind_speed": {
            "average": data.get("av_ws", {}).get("av"),
            "min": data.get("av_ws", {}).get("mn"),
            "max": data.get("av_ws", {}).get("mx"),
        },
        "wind_direction": (data.get("wd") or {}).get("most_common", {}).get("compass_point"),
    }

    return weather

def _fmt(val, spec):
    return format(val, spec) if val is not None else "N/A"


def display_weather(weather):
    """Display formatted weather data"""
    if not weather:
        print("No weather data available")
        return

    print("\n" + "="*50)
    print("MARS WEATHER DATA")
    print("="*50)
    sol = weather.get('sol')
    print(f"Last Updated: {weather['timestamp']}")
    if sol:
        print(f"Mars Sol: {sol}\n")
    else:
        print()

    temp = weather['temperature']
    print("Temperature (°C)")
    print(f"  Average: {_fmt(temp['average'], '.1f')}°C")
    print(f"  Min: {_fmt(temp['min'], '.1f')}°C")
    print(f"  Max: {_fmt(temp['max'], '.1f')}°C\n")

    pressure = weather['pressure']
    print("Pressure (Pa)")
    print(f"  Average: {_fmt(pressure['average'], '.2f')}")
    print(f"  Min: {_fmt(pressure['min'], '.2f')}")
    print(f"  Max: {_fmt(pressure['max'], '.2f')}\n")

    wind = weather['wind_speed']
    print("Wind Speed (m/s)")
    print(f"  Average: {_fmt(wind['average'], '.2f')}")
    print(f"  Min: {_fmt(wind['min'], '.2f')}")
    print(f"  Max: {_fmt(wind['max'], '.2f')}\n")

    print(f"Prevailing Wind Direction: {weather['wind_direction'] or 'Unknown'}\n")

def main():
    """Main function"""
    print("Fetching Mars weather data...")
    data = fetch_mars_weather()
    
    if data:
        weather = parse_weather_data(data)
        display_weather(weather)
        print("Data format for Home Assistant REST sensor:")
        print(json.dumps(weather, indent=2))
    else:
        print("Failed to fetch Mars weather data", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
