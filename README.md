# NASA Mars Weather to Home Assistant

Display real-time Mars weather data from NASA's InSight Mars Weather Service in Home Assistant.

## Installation

### Method 1: HACS Custom Repository (Recommended)

1. Open Home Assistant → **HACS** → **Integrations**
2. Click the **⋯** (three dots) menu in the top right
3. Select **Custom repositories**
4. Paste this URL: `https://github.com/St3inberg/nasa-weather`
5. Select **Integration** as the category
6. Click **Create**
7. Now search for **NASA Mars Weather** in HACS
8. Click **Download**
9. Restart Home Assistant
10. Go to **Settings** → **Devices & Services**
11. Click **Create Integration** (or **+** button)
12. Search for **NASA Mars Weather**
13. Enter your NASA API key and click **Submit**

### Method 2: Manual Installation

1. Download the repository
2. Copy `custom_components/nasa_mars_weather` to your Home Assistant `custom_components` folder
3. Restart Home Assistant
4. Go to **Settings** → **Devices & Services** → **Create Integration**
5. Search for **NASA Mars Weather**
6. Enter your NASA API key

## Get Your NASA API Key

Free API keys available at: https://api.nasa.gov/

1. Go to https://api.nasa.gov/
2. Fill out the form with your details
3. You'll receive your API key via email

## Configuration

After installation, the integration will prompt you for your NASA API key in the Home Assistant UI. No manual configuration.yaml editing required!

## Legacy Setup (Manual REST Sensor)

### 1. NASA API Key
Get your free API key at: https://api.nasa.gov/

- **API Documentation**: https://api.nasa.gov/
- **Mars Weather Endpoint**: `https://api.nasa.gov/insight_weather/?feedtype=json&ver=1.0&api_key={YOUR_API_KEY}`

### 2. Home Assistant REST Sensor Configuration

Add the following to your Home Assistant `configuration.yaml`:

```yaml
rest:
  - resource: https://api.nasa.gov/insight_weather/?feedtype=json&ver=1.0&api_key=YOUR_NASA_API_KEY_HERE
    scan_interval: 3600
    sensor:
      - name: "Mars Temperature"
        unique_id: mars_temp
        unit_of_measurement: "°C"
        value_template: "{{ value_json.av_t.av | round(1) }}"
        
      - name: "Mars Min Temperature"
        unique_id: mars_min_temp
        unit_of_measurement: "°C"
        value_template: "{{ value_json.av_t.mn | round(1) }}"
        
      - name: "Mars Max Temperature"
        unique_id: mars_max_temp
        unit_of_measurement: "°C"
        value_template: "{{ value_json.av_t.mx | round(1) }}"
        
      - name: "Mars Pressure"
        unique_id: mars_pressure
        unit_of_measurement: "Pa"
        value_template: "{{ value_json.av_p.av | round(1) }}"
        
      - name: "Mars Wind Speed"
        unique_id: mars_wind
        unit_of_measurement: "m/s"
        value_template: "{{ value_json.av_ws.av | round(2) }}"
```

### 3. Alternative: Using Python Script

See `fetch_mars_weather.py` for a standalone script to fetch and log Mars weather data.

### 4. API Rate Limits
- **Hourly Limit**: 1,000 requests per hour
- **Recommended Refresh**: 3600 seconds (1 hour)

## Data Available

The API returns:
- Average temperature (`av_t.av`)
- Min/Max temperatures (`av_t.mn`, `av_t.mx`)  
- Pressure (`av_p.av`)
- Wind speed (`av_ws.av`)
- Wind direction (`wd.most_common`)

## Home Assistant Lovelace Card Example

```yaml
type: entities
title: Mars Weather
entities:
  - entity: sensor.mars_temperature
  - entity: sensor.mars_min_temperature
  - entity: sensor.mars_max_temperature
  - entity: sensor.mars_pressure
  - entity: sensor.mars_wind_speed
```

## Resources
- [NASA API Portal](https://api.nasa.gov/)
- [Home Assistant REST Integration](https://www.home-assistant.io/integrations/rest/)
- [Home Assistant Template](https://www.home-assistant.io/docs/configuration/templating/)
