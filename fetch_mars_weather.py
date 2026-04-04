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

def fetch_mars_weather():
    """Fetch latest Mars weather data from NASA API"""
    api_key = os.environ.get("NASA_API_KEY")
    
    if not api_key:
        print("Error: NASA_API_KEY environment variable not set", file=sys.stderr)
        return None
    
    params = {
        "feedtype": "json",
        "ver": "1.0",
        "api_key": api_key
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return None

def parse_weather_data(data):
    """Parse and format weather data"""
    if not data or "av_t" not in data:
        return None
    
    weather = {
        "timestamp": datetime.now().isoformat(),
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
        "wind_direction": data.get("wd", {}).get("most_common", {}).get("compass_point"),
    }
    
    return weather

def display_weather(weather):
    """Display formatted weather data"""
    if not weather:
        print("No weather data available")
        return
    
    print("\n" + "="*50)
    print("MARS WEATHER DATA")
    print("="*50)
    print(f"Last Updated: {weather['timestamp']}\n")
    
    print("Temperature (°C)")
    print(f"  Average: {weather['temperature']['average']:.1f}°C")
    print(f"  Min: {weather['temperature']['min']:.1f}°C")
    print(f"  Max: {weather['temperature']['max']:.1f}°C\n")
    
    print("Pressure (Pa)")
    print(f"  Average: {weather['pressure']['average']:.2f}")
    print(f"  Min: {weather['pressure']['min']:.2f}")
    print(f"  Max: {weather['pressure']['max']:.2f}\n")
    
    print("Wind Speed (m/s)")
    print(f"  Average: {weather['wind_speed']['average']:.2f}")
    print(f"  Min: {weather['wind_speed']['min']:.2f}")
    print(f"  Max: {weather['wind_speed']['max']:.2f}\n")
    
    print(f"Prevailing Wind Direction: {weather['wind_direction']}\n")

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
