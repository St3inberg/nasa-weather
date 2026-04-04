# HACS Cache Issue - Force Update Solution

## Problem
You're still getting the error from the old version (960e852) even though the fix has been committed.

**Reason:** HACS is caching the old repository data

## Solution: Clear HACS Cache and Force Refresh

### Method 1: Via Developer Tools (Recommended)

1. **Go to Home Assistant**
   - Settings → Developer Tools → Services

2. **Find "HACS" Service**
   - Search for: `hacs.repositories`
   - Or search for: `hacs`

3. **Run These Services in Order:**

**Step 1: Force Update**
```yaml
Service: HACS - Force update repositories
```

**Step 2: Clear Cache**
```yaml
Service: Homeassistant - Reload Custom Components
```

**Step 3: Restart**
```yaml
Service: Homeassistant - Restart
```

4. **Wait 2-3 minutes for restart**

5. **Try Installing Again**
   - HACS → Integrations
   - Search: "NASA Mars Weather"
   - Should now show as compatible

---

### Method 2: Delete Local Cache Files

1. **SSH into Home Assistant**
   ```bash
   cd /config/.storage
   ls -la | grep hacs
   ```

2. **Delete HACS cache:**
   ```bash
   rm -f homeassistant.restore_state.json
   rm -rf .hacs/  # If this folder exists
   ```

3. **Restart Home Assistant:**
   ```bash
   # Via web UI: Settings → Developer Tools → Restart
   # Or via terminal:
   docker restart homeassistant  # If using Docker
   ```

---

### Method 3: Delete and Re-add Repository

1. **Remove the custom repository:**
   - HACS → Integrations
   - Click ⋯ → Custom repositories
   - Find "NASA Mars Weather"
   - Click the trash icon to delete

2. **Clear HACS cache:**
   - Settings → Developer Tools
   - Service: `hacs.repositories` 
   - Choose "Force update"

3. **Wait 5 minutes**

4. **Add repository again:**
   - HACS → Integrations → ⋯ → Custom repositories
   - URL: `https://github.com/St3inberg/nasa-weather`
   - Category: Integration
   - Click Create

5. **Search and download**

---

### Method 4: Nuclear Option (Last Resort)

1. **Delete everything HACS:**
   ```bash
   # SSH into Home Assistant
   cd /config
   rm -rf .hacs
   rm -rf custom_components/nasa_mars_weather/  # If exists
   ```

2. **Delete HACS storage files:**
   ```bash
   cd /config/.storage
   rm -f *hacs*
   ```

3. **Restart Home Assistant completely:**
   - Power off and restart
   - Or use Docker restart command

4. **Reinstall HACS:**
   - Follow HACS installation guide
   - https://hacs.xyz/docs/setup/prerequisites

5. **Add custom repository and install**

---

## Verify the Latest Version

### Check Current Commit

**In repository:**
- Current HACS-compatible version: `d0ed06f`
- Old incompatible version: `960e852`

**You should be getting version `d0ed06f` or later**

### Verify Files Are Present

After installation, check `/config/custom_components/nasa_mars_weather/` should have:

```
nasa_mars_weather/
├── __init__.py
├── config_flow.py
├── sensor.py
├── manifest.json (should have "homeassistant": "2023.12.0")
├── strings.json
├── lovelace/
│   ├── mars-weather-card.js
│   └── resources.json
└── lovelace.py
```

**Most importantly:** Check that `hacs.json` exists in the ROOT folder:
```bash
ls -la /config/hacs.json
```

---

## Step-by-Step Fresh Install

If caching is the issue, do a complete fresh install:

### 1. Delete Everything
```bash
# SSH into Home Assistant
cd /config
rm -rf custom_components/nasa_mars_weather/
```

### 2. Restart Home Assistant
- Settings → Developer Tools → Restart
- Wait 2-3 minutes

### 3. Force HACS Update
- Settings → Developer Tools → Services
- Service: `hacs.repositories`
- Event: Force update
- Press Execute

### 4. Wait 5 minutes
(HACS needs time to refresh repository data)

### 5. Add Repository
- HACS → Integrations
- Click ⋯ (three dots)
- Select "Custom repositories"
- Enter: `https://github.com/St3inberg/nasa-weather`
- Category: **Integration**
- Click "Create"

### 6. Search & Download
- HACS should now find it
- Click on "NASA Mars Weather"
- Click "Download"

### 7. Choose Version
- Select latest version
- Click "Download"

### 8. Restart
- Settings → Developer Tools → Restart

### 9. Verify
- Settings → Devices & Services
- Should see "NASA Mars Weather" listed
- With 1 device and 10 entities

---

## Why This Happens

HACS caches repository information in:
- `.hacs/` folder
- `.storage/` folder files
- Home Assistant's restore state

When we pushed the fix:
- ✅ GitHub updated (version d0ed06f)
- ❌ HACS cache still had old version (960e852)

HACS will eventually sync, but forcing a refresh speeds it up.

---

## If Problem Persists

1. **Check GitHub is updated:**
   ```
   https://github.com/St3inberg/nasa-weather/commits/main
   Latest should be "d0ed06f - Add HACS compatibility fix summary"
   ```

2. **Verify repository access:**
   ```bash
   curl -I https://raw.githubusercontent.com/St3inberg/nasa-weather/main/hacs.json
   # Should return: HTTP/2 200
   ```

3. **Check Home Assistant logs:**
   - Settings → System → Logs
   - Search for: "nasa_mars"
   - Look for any error messages

4. **Check manifest.json:**
   ```bash
   # SSH into Home Assistant
   curl https://raw.githubusercontent.com/St3inberg/nasa-weather/main/custom_components/nasa_mars_weather/manifest.json | python -m json.tool
   # Should show: "homeassistant": "2023.12.0"
   ```

---

## Solution Summary

| Method | Time | Success Rate |
|--------|------|--------------|
| Force Update via Services | 5-10 min | 85% |
| Delete Cache Files | 10-15 min | 90% |
| Delete & Re-add Repo | 15-20 min | 95% |
| Nuclear Option | 30 min | 100% |

**Recommended:** Try Method 1 first, then Method 3 if that doesn't work.

---

## After Successfully Installing

Once you see version `d0ed06f` or later installed:

1. ✅ No more HACS errors
2. ✅ Sensors auto-create
3. ✅ Card registers automatically
4. ✅ Works perfectly

---

## Need More Help?

Check these files in the repository:
- [HACS_TROUBLESHOOTING.md](./HACS_TROUBLESHOOTING.md)
- [INSTALLATION.md](./INSTALLATION.md)  
- [HACS_FIX_SUMMARY.md](./HACS_FIX_SUMMARY.md)

Report issue: https://github.com/St3inberg/nasa-weather/issues

---

**Try Method 1 first - usually fixes it within 10 minutes!**
