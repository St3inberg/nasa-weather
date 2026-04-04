# Quick Start Guide - NASA Mars Weather

Get real-time Mars weather in your Home Assistant with a beautiful dashboard card in 5 minutes!

## 📋 Prerequisites

- Home Assistant installed and running
- HACS installed (https://hacs.xyz/)
- NASA API key (free from https://api.nasa.gov/)

## 🚀 Installation Steps

### Step 1: Add Custom Repository to HACS

1. Open Home Assistant
2. Go to **HACS** → **Integrations**
3. Click the **⋯** menu → **Custom repositories**
4. Enter: `https://github.com/St3inberg/nasa-weather`
5. Select category: **Integration**
6. Click **Create**

### Step 2: Install the Integration

1. Search for **NASA Mars Weather** in HACS
2. Click on it
3. Click **Download**
4. Choose version (latest recommended)
5. Click **Download**
6. Restart Home Assistant

### Step 3: Configure the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **Create Integration** (or **+** button)
3. Search for **NASA Mars Weather**
4. Enter your NASA API key
5. Click **Submit**

### Step 4: Add the Card to Your Dashboard

1. Go to your Home Assistant dashboard
2. Click **Edit Dashboard** (pencil icon)
3. Click **Add Card**
4. Select **Manual** (or use UI editor)
5. Add this YAML:

```yaml
type: custom:mars-weather-card
entity: sensor.mars_avg_temperature
```

6. Click **Save**

## ✨ That's It!

Your Mars weather card is now live with:
- 🔴 Mars-themed background
- 📊 Real-time temperature, pressure, wind data
- 📱 Mobile-friendly responsive design
- ⚡ Updates every hour from NASA

## 📍 What You'll See

| Data | Unit | Range |
|------|------|-------|
| Temperature | °C | -100 to 30 |
| Pressure | Pa | 600-700 |
| Wind Speed | m/s | 0-20 |
| Wind Direction | Compass | All directions |

## 🎨 Card Features

- **Mars Background**: Gradient background mimics Mars surface
- **Real-time Data**: Displays current weather from NASA InSight
- **Animations**: Floating elements for visual appeal
- **Responsive**: Works on desktop, tablet, and mobile
- **Live Updates**: Automatically refreshes every hour

## 📊 Creating More Complex Dashboards

### Temperature History

```yaml
type: history-graph
entities:
  - sensor.mars_avg_temperature
title: "Mars Temperature (Last 48h)"
```

### Weather Gauges

```yaml
type: grid
cards:
  - type: gauge
    entity: sensor.mars_avg_temperature
    min: -100
    max: 30
    title: "Temperature"
    
  - type: gauge
    entity: sensor.mars_avg_pressure
    min: 600
    max: 700
    title: "Pressure"
```

### Complete Dashboard View

```yaml
views:
  - title: Mars Station
    path: mars
    icon: mdi:planet
    cards:
      - type: heading
        heading: "🔴 Mars Weather Station"
        
      - type: custom:mars-weather-card
        entity: sensor.mars_avg_temperature
        
      - type: history-graph
        entities:
          - sensor.mars_avg_temperature
          - sensor.mars_avg_wind_speed
```

## 🔧 Available Sensors

These sensors are automatically created:

- `sensor.mars_avg_temperature` - Current temperature
- `sensor.mars_min_temperature` - Min temperature
- `sensor.mars_max_temperature` - Max temperature
- `sensor.mars_avg_pressure` - Current pressure
- `sensor.mars_avg_wind_speed` - Wind speed
- `sensor.mars_wind_direction` - Wind direction

## ❓ Troubleshooting

### Card Not Appearing?

```
1. Check Settings → Developer Tools → States
2. Look for sensors starting with "sensor.mars_"
3. If missing, check integration status
4. Try restarting Home Assistant
```

### No Data?

```
1. Verify API key is correct and not expired
2. Check Settings → Devices & Services → NASA Mars Weather
3. View integration logs for errors
4. NASA API must be accessible (https://api.nasa.gov/)
```

### Browser Cache Issue?

```
- Clear cache: Ctrl+F5 (Windows/Linux) or Cmd+Shift+R (Mac)
- Or use incognito/private mode to test
```

## 💡 Pro Tips

1. **Automation**: Create automations based on Mars wind or temperature
2. **History**: Use history-graph to track weather changes
3. **Mobile**: Card works great on phones
4. **Multiple Cards**: Add multiple cards for different metrics
5. **Customize**: Edit the card styling in the integration folder

## 📖 Learn More

- **Card Documentation**: See [LOVELACE.md](LOVELACE.md)
- **Testing Guide**: See [TESTING.md](TESTING.md)
- **Full README**: See [README.md](README.md)
- **Mars Weather Data**: https://api.nasa.gov/

## 🐛 Found an Issue?

Report bugs: https://github.com/St3inberg/nasa-weather/issues

## ⭐ Show Your Support

If you love this integration, give it a star on GitHub!

---

**Enjoy your Mars weather dashboard! 🔴🌍**
