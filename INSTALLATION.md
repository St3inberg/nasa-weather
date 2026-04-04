# Installation Guide

## Home Assistant Integration Installation

### Method 1: HACS (Recommended)

#### Prerequisites
- Home Assistant 2023.12.0 or later
- HACS installed (https://hacs.xyz/docs/setup/prerequisites)
- NASA API key (free from https://api.nasa.gov/)

#### Step-by-Step Installation

1. **Add Custom Repository to HACS**
   - Open Home Assistant
   - Go to HACS → Integrations
   - Click the three dots (⋯) menu → "Custom repositories"
   - URL: `https://github.com/St3inberg/nasa-weather`
   - Category: Select "Integration"
   - Click "Create"

2. **Install the Integration**
   - Search for "NASA Mars Weather" in HACS
   - Click on the result
   - Click "Download"
   - Choose the latest version
   - Click "Download" confirm
   - Wait for download to complete

3. **Restart Home Assistant**
   - Go to Settings → Developer Tools
   - Click "Restart" (or restart manually)
   - Wait for Home Assistant to restart (1-2 minutes)

4. **Configure the Integration**
   - Go to Settings → Devices & Services
   - Click "Create Integration" (+ button in bottom right)
   - Search for "NASA Mars Weather"
   - Enter your NASA API key
   - Click "Submit"
   - The integration will validate your API key

5. **Add the Card to Your Dashboard**
   - Edit your dashboard (pencil icon)
   - Click "Add Card"
   - Select "Manual" or search for `mars-weather-card`
   - Enter the configuration:
     ```yaml
     type: custom:mars-weather-card
     entity: sensor.mars_avg_temperature
     ```
   - Click "Save"

### Method 2: Manual Installation

#### For Developers

1. **Download the Integration**
   ```bash
   cd /path/to/your/home-assistant-config
   mkdir -p custom_components
   git clone https://github.com/St3inberg/nasa-weather.git
   cp -r nasa-weather/custom_components/nasa_mars_weather custom_components/
   ```

2. **Restart Home Assistant**
   - Settings → Developer Tools → Restart

3. **Add Integration**
   - Settings → Devices & Services → Create Integration
   - Search for "NASA Mars Weather"
   - Enter your API key

### Method 3: Docker Installation

```bash
# If using Home Assistant in Docker
docker exec homeassistant /bin/bash -c "cd /config && git clone https://github.com/St3inberg/nasa-weather.git && cp -r nasa-weather/custom_components/nasa_mars_weather custom_components/"

# Restart the container
docker restart homeassistant
```

## Troubleshooting Installation Issues

### Issue: "Can't find integration" in HACS

**Solution:**
1. Clear HACS cache:
   - Settings → Developer Tools → Services → `hacs.repositories`
   - Search for "hacs" and look for cache clear option
2. Refresh HACS page (F5)
3. Try adding the custom repository again

### Issue: Integration doesn't appear after restart

**Solution:**
1. Check Home Assistant logs:
   - Settings → Developer Tools → Logs
   - Search for "nasa_mars_weather"
2. Verify files are in correct location:
   ```
   /config/custom_components/nasa_mars_weather/
   ```
3. Check manifest.json is valid JSON:
   - Use online JSON validator
   - Ensure no trailing commas

### Issue: "Invalid API key" error

**Solution:**
1. Verify API key from https://api.nasa.gov/
2. Check if API key is valid (not expired)
3. Try again - sometimes NASA API needs time to activate keys
4. Check internet connection

### Issue: Card not showing in dashboard

**Solution:**
1. Refresh browser (Ctrl+F5 or Cmd+Shift+R)
2. Clear browser cache
3. Verify entity exists:
   - Developer Tools → States
   - Search for "mars_avg_temperature"
4. Check browser console (F12) for errors

### Issue: "HACS version cannot be used"

**Solution:**
This usually means:
1. Manifest.json is not properly formatted
2. Missing required HACS fields
3. Repository structure is incorrect

**Fix:**
1. Delete the custom_components folder
2. Restart Home Assistant
3. Install again from HACS

## Verifying Installation

After installation, verify everything is working:

1. **Check Integration Status**
   - Settings → Devices & Services
   - Look for "NASA Mars Weather" entry
   - Should show 1 device with 10 entities

2. **Verify Sensors**
   - Developer Tools → States
   - Search for "sensor.mars"
   - Should see 10 sensors listed

3. **Check Card Registration**
   - Settings → Devices & Services → NASA Mars Weather
   - Card should be registered automatically

4. **Test Dashboard Card**
   - Create/edit dashboard
   - Add card: `type: custom:mars-weather-card`
   - Should display with Mars background

## Post-Installation

### First Steps
1. ✅ Add the integration (done above)
2. ✅ Add the Lovelace card to a dashboard
3. ✅ Create automations based on Mars weather
4. ✅ Enjoy real Mars weather data!

### Recommended Automations
```yaml
# Alert when Mars is very cold
automation:
  - alias: "Mars Very Cold Alert"
    trigger:
      platform: numeric_state
      entity_id: sensor.mars_avg_temperature
      below: -80
    action:
      service: notify.notify
      data:
        message: "Mars temperature dropped below -80°C!"
```

### Optional Customizations
- Edit card colors in `mars-weather-card.js`
- Add to multiple dashboards
- Create custom history graphs
- Use in conditional cards

## Getting Your API Key

If you don't have a NASA API key yet:

1. Go to https://api.nasa.gov/
2. Fill out the form:
   - First Name (required)
   - Last Name (required)
   - Email (required)
   - Application Name: "Home Assistant Mars Weather"
   - How will you use the APIs: "Home automation and display"
3. Click "Signup"
4. Check your email for the API key
5. Use it in Home Assistant setup

**Free API Key Benefits:**
- 1,000 requests per hour limit
- No cost
- Instant activation
- Mars weather data access

## Support

If you encounter issues:

1. Check [QUICKSTART.md](./QUICKSTART.md) for getting started
2. See [LOVELACE.md](./LOVELACE.md) for card help
3. Review [TESTING.md](./TESTING.md) for testing
4. Report issues: https://github.com/St3inberg/nasa-weather/issues

## Version History

### Version 1.0.0 (Current)
- ✅ Initial release
- ✅ 10 sensors for Mars weather data
- ✅ Lovelace card with Mars theme
- ✅ HACS support
- ✅ Comprehensive testing
- ✅ Full documentation

## Next Steps

Once installed:
1. View Mars weather on your dashboard
2. Create automations using the sensors
3. Explore historical data
4. Customize the card appearance
5. Share your setup with the community!

---

**Enjoy your Mars Weather integration! 🔴**
