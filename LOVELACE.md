# Mars Weather Lovelace Card

A beautiful, Mars-themed custom Lovelace card for displaying NASA Mars Weather data in Home Assistant.

## Features

- 🔴 Mars-themed gradient background
- 📊 Real-time weather data display
- 🎨 Beautiful glass-morphism design with animations
- 📱 Fully responsive layout
- 🌐 Works with Home Assistant Lovelace dashboard

## Installation

The card is automatically installed when you add the **NASA Mars Weather** integration to Home Assistant.

### Manual Installation

If you need to manually register the card:

1. Go to **Settings** → **Dashboards** → **Lovelace Resources**
2. Click **Create Resource**
3. Enter URL: `/custom_components/nasa_mars_weather/lovelace/mars-weather-card.js`
4. Select Type: **JavaScript Module**
5. Click **Create**

## Usage

### Basic Card

```yaml
type: custom:mars-weather-card
entity: sensor.mars_avg_temperature
```

### Full Configuration Example

```yaml
type: vertical-stack
cards:
  - type: custom:mars-weather-card
    entity: sensor.mars_avg_temperature
    title: "Mars Weather Station"
    
  - type: entities
    title: "Mars Sensors"
    entities:
      - sensor.mars_avg_temperature
      - sensor.mars_min_temperature
      - sensor.mars_max_temperature
      - sensor.mars_avg_pressure
      - sensor.mars_avg_wind_speed
      - sensor.mars_wind_direction
```

### In Dashboard Editor (YAML Mode)

1. Open your Home Assistant dashboard
2. Click **Edit Dashboard** (pencil icon)
3. Click **Add Card**
4. Select **Manual** → **By entity**
5. Create a new card with type: `custom:mars-weather-card`
6. Set the entity to your Mars temperature sensor

## Card Configuration Options

```yaml
type: custom:mars-weather-card
entity: sensor.mars_avg_temperature        # Required: Temperature sensor entity
title: "Mars Weather"                       # Optional: Card title
show_stats: true                            # Optional: Show statistics
```

## Dashboard Examples

### Minimal Dashboard

```yaml
views:
  - title: Space
    path: space
    cards:
      - type: custom:mars-weather-card
        entity: sensor.mars_avg_temperature
```

### Complete Mars Weather Dashboard

```yaml
views:
  - title: Mars Weather
    path: mars
    icon: mdi:planet
    cards:
      - type: heading
        heading: "🔴 Mars Weather Station"
        
      - type: custom:mars-weather-card
        entity: sensor.mars_avg_temperature
        
      - type: grid
        cards:
          - type: gauge
            entity: sensor.mars_avg_temperature
            min: -100
            max: 30
            
          - type: gauge
            entity: sensor.mars_avg_pressure
            min: 600
            max: 700
            
          - type: gauge
            entity: sensor.mars_avg_wind_speed
            min: 0
            max: 10
            
      - type: history-graph
        entities:
          - sensor.mars_avg_temperature
          - sensor.mars_avg_pressure
        title: "Mars Weather History"
```

## Card Styling

The card uses CSS variables for theming:

```css
--mars-bg: linear-gradient(135deg, #c1440e 0%, #8b3a0c 50%, #4a1f05 100%);
--mars-dark: #3d1a04;
--mars-accent: #e67e22;
```

To customize, edit `mars-weather-card.js` and modify the CSS variables.

## Sensors Available

The integration creates these sensors that can be used in the card:

- `sensor.mars_avg_temperature` - Average temperature (°C)
- `sensor.mars_min_temperature` - Minimum temperature (°C)
- `sensor.mars_max_temperature` - Maximum temperature (°C)
- `sensor.mars_avg_pressure` - Average pressure (Pa)
- `sensor.mars_min_pressure` - Minimum pressure (Pa)
- `sensor.mars_max_pressure` - Maximum pressure (Pa)
- `sensor.mars_avg_wind_speed` - Average wind speed (m/s)
- `sensor.mars_min_wind_speed` - Minimum wind speed (m/s)
- `sensor.mars_max_wind_speed` - Maximum wind speed (m/s)
- `sensor.mars_wind_direction` - Prevailing wind direction

## Troubleshooting

### Card Not Showing

1. Check if you see `custom:mars-weather-card` in Lovelace Resources
2. Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
3. Reload Lovelace dashboard
4. Check browser console for errors (F12)

### Entities Not Showing

1. Verify the entity ID is correct
2. Check **Developer Tools** → **States** to see available entities
3. Ensure the NASA Mars Weather integration is loaded
4. Check integration status in **Settings** → **Devices & Services**

### No Data Displayed

1. Verify NASA API key is valid
2. Check integration logs in **Settings** → **Devices & Services** → Mars Weather
3. Ensure Mars weather API is responding (https://api.nasa.gov/)

## Customization

### Adding Text or Icons

Edit `mars-weather-card.js` to add custom content to the card:

```javascript
// Add custom HTML in the render function
<div class="custom-section">
  Your custom content here
</div>
```

### Changing Colors

Update the CSS variables at the top of `mars-weather-card.js`:

```css
--mars-bg: linear-gradient(135deg, #your-color 0%, ...);
--mars-accent: #your-accent-color;
```

## Browser Compatibility

- Chrome/Edge 76+
- Firefox 67+
- Safari 13+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Support

For issues or feature requests, visit: https://github.com/St3inberg/nasa-weather/issues

## License

Same as the NASA Mars Weather integration
