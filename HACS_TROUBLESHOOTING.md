# HACS Troubleshooting Guide

## Common HACS Installation Issues

### Issue 1: Integration Not Found in HACS

**Error Message:** "Cannot find NASA Mars Weather in HACS"

**Causes:**
- Custom repository not added
- Repository URL incorrect
- HACS not loading the repository

**Solutions:**

```bash
# Method 1: Re-add custom repository
1. Settings → HACS → Integrations
2. Click ⋯ (three dots)
3. Select "Custom repositories"
4. Add: https://github.com/St3inberg/nasa-weather
5. Category: Integration
6. Click "Create"
```

Or check home-assistant logs:
```
Settings → Developer Tools → Logs
Search for: "nasa_mars_weather"
```

---

### Issue 2: "Integration version cannot be used with HACS"

**Error Message:** "The version X of nasa_mars_weather cannot be used with HACS"

**Root Cause:** 
- Missing `hacs.json` in repository root
- Invalid manifest.json format
- Missing required fields

**Solution:**
This should now be fixed! We added:
- ✅ `hacs.json` with proper metadata
- ✅ Updated `manifest.json` with homeassistant version
- ✅ Added `iot_class` field
- ✅ Added `platforms` field

**If error persists:**
1. Delete the integration folder
2. Restart Home Assistant
3. Clear HACS cache:
   ```yaml
   # Developer Tools → Services
   Service: HACS - Force update repositories
   ```
4. Install again

---

### Issue 3: Integration Fails to Load After Installation

**Error in Logs:**
```
ERROR (MainThread) [homeassistant.loader] Error loading nasa_mars_weather
Unexpected error loading integration nasa_mars_weather
```

**Causes:**
- Files not in correct location
- Missing dependencies
- Python syntax errors
- Home Assistant restart needed

**Solutions:**

1. **Verify File Location:**
   ```
   /config/custom_components/nasa_mars_weather/
   ├── __init__.py
   ├── config_flow.py
   ├── sensor.py
   ├── manifest.json
   ├── strings.json
   └── lovelace/
       └── mars-weather-card.js
   ```

2. **Restart Home Assistant:**
   ```
   Settings → Developer Tools → Restart
   ```
   (Full restart, not just reloading)

3. **Check Python Syntax:**
   ```bash
   python -m py_compile /config/custom_components/nasa_mars_weather/*.py
   ```

4. **Check manifest.json:**
   ```bash
   python -m json.tool /config/custom_components/nasa_mars_weather/manifest.json
   ```

---

### Issue 4: Sensors Not Creating

**Symptom:** Integration loads but no sensors appear

**Causes:**
- Integration not fully loaded
- API key validation failed
- Coordinator not updating

**Solutions:**

1. **Check Entity Creation:**
   ```
   Developer Tools → States
   Search: "mars"
   ```
   Should show 10 entities

2. **Check Integration Status:**
   ```
   Settings → Devices & Services
   Find: "NASA Mars Weather"
   Click on it to see status
   ```

3. **View Integration Logs:**
   ```
   Settings → Devices & Services → NASA Mars Weather
   Click three dots → Logs
   ```

4. **Verify API Key:**
   - Go to https://api.nasa.gov/
   - Check API key is valid
   - Try making a test request:
     ```
     https://api.nasa.gov/insight_weather/?api_key=YOUR_KEY&feedtype=json&ver=1.0
     ```

---

### Issue 5: Lovelace Card Not Available

**Symptom:** Can't find `mars-weather-card` in card selector

**Causes:**
- Card not registered with Lovelace
- Browser cache issue
- Missing JavaScript file

**Solutions:**

1. **Verify Card File Exists:**
   ```
   /config/custom_components/nasa_mars_weather/lovelace/mars-weather-card.js
   ```

2. **Clear Browser Cache:**
   ```
   Ctrl+F5 (Windows/Linux)
   Cmd+Shift+R (Mac)
   ```

3. **Reload Lovelace Resources:**
   ```
   Developer Tools → Services
   Service: Lovelace - Reload resources
   ```

4. **Check Browser Console:**
   ```
   F12 → Console
   Look for JavaScript errors
   ```

5. **Manual Card Addition:**
   ```yaml
   type: custom:mars-weather-card
   entity: sensor.mars_avg_temperature
   ```

---

### Issue 6: API Key Validation Fails

**Error Message:** "Failed to connect to NASA API" or "Invalid API key"

**Causes:**
- API key not valid
- Internet connection issue
- NASA API temporarily down
- Rate limit exceeded

**Solutions:**

1. **Verify API Key:**
   ```
   https://api.nasa.gov/insight_weather/?api_key=YOUR_KEY&feedtype=json&ver=1.0
   ```
   Should return JSON data

2. **Check Internet:**
   ```bash
   ping api.nasa.gov
   curl -I https://api.nasa.gov/
   ```

3. **Wait and Retry:**
   - Sometimes new API keys need time to activate
   - Wait 30 minutes and try again

4. **Check Rate Limits:**
   - 1,000 requests per hour
   - 30-50 requests per day with demo key
   - Use your own API key for higher limits

5. **Reset the Integration:**
   ```
   Settings → Devices & Services
   Find NASA Mars Weather
   Click three dots → Delete
   Restart Home Assistant
   Add integration again with new key
   ```

---

### Issue 7: HACS Shows Update Available But Won't Install

**Symptom:** "Update available" notification but installation fails

**Solution:**

1. **Delete the entire integration:**
   ```bash
   rm -r /config/custom_components/nasa_mars_weather/
   ```

2. **Restart Home Assistant:**
   ```
   Settings → Developer Tools → Restart
   ```

3. **Reinstall from HACS:**
   - Search for NASA Mars Weather
   - Download latest version
   - Restart Home Assistant

---

## Diagnostic Commands

### Check Integration Status
```yaml
# Developer Tools → Services
Service: Homeassistant - Check config
```

### View Entity Details
```
Developer Tools → States
Filter: "mars"
```

### Check System Logs
```
Settings → System → Logs
Download full logs
Look for: "nasa_mars_weather"
```

### Test API Connection
```bash
# From command line
curl -s "https://api.nasa.gov/insight_weather/?api_key=YOUR_KEY&feedtype=json&ver=1.0" | jq .
```

---

## Debug Mode

Enable debug logging:

**Method 1: Via Configuration**
```yaml
# Add to configuration.yaml
logger:
  logs:
    custom_components.nasa_mars_weather: debug
```

**Method 2: Via Developer Tools**
```yaml
# Developer Tools → Services
Service: Logger - Set level
Data:
  custom_components.nasa_mars_weather: debug
```

Then check logs:
```
Settings → Developer Tools → Logs
```

---

## Performance Issues

### Integration Loading Slowly

**Causes:**
- Network issues with NASA API
- Too many sensor updates
- Home Assistant resource constraints

**Solutions:**
1. Check internet speed
2. Verify NASA API is responding
3. Increase update interval in integration settings
4. Check Home Assistant resource usage

### High CPU Usage

**Solution:**
- Integration uses minimal CPU
- If high CPU, check Home Assistant system
- May be other integrations or automations

---

## Rollback to Previous Version

If new version has issues:

```bash
# In /config/custom_components/nasa_mars_weather
cd /config/custom_components/nasa_mars_weather
git log --oneline  # See commit history
git checkout COMMIT_ID  # Go to previous version
```

Or reinstall specific version in HACS

---

## Getting Help

### Before Reporting an Issue

1. ✅ Read this guide completely
2. ✅ Check Home Assistant version (2023.12.0+)
3. ✅ Verify NASA API key works
4. ✅ Check browser console for errors
5. ✅ Review integration logs
6. ✅ Try deleting and reinstalling

### Report an Issue

Include:
- Home Assistant version
- HACS version
- Error messages from logs
- Steps to reproduce
- Browser type and version
- Full integration configuration (without API key)

**Report here:** https://github.com/St3inberg/nasa-weather/issues

---

## Quick Fix Checklist

- [ ] Home Assistant restarted?
- [ ] Files in correct location?
- [ ] manifest.json valid?
- [ ] API key correct?
- [ ] NASA API responding?
- [ ] Browser cache cleared?
- [ ] HACS cache cleared?
- [ ] Integration shows in Devices & Services?
- [ ] Sensors showing in Developer Tools → States?
- [ ] Lovelace card loads without errors?

If all checked, integration should work!

---

## Success Indicators

You know it's working when:

✅ Integration appears in Settings → Devices & Services
✅ 10 sensors appear in Developer Tools → States
✅ Card shows Mars weather on dashboard
✅ Temperature value displays (not "Unknown")
✅ Data updates every hour
✅ No errors in system logs

---

**Having trouble? Start with [INSTALLATION.md](./INSTALLATION.md) or [QUICKSTART.md](./QUICKSTART.md)**
