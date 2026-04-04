"""NASA Mars Weather Integration for Home Assistant"""

import logging
from datetime import timedelta

import requests
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nasa_mars_weather"
PLATFORMS = [Platform.SENSOR]
SCAN_INTERVAL = timedelta(hours=1)


class MarsWeatherUpdateCoordinator(DataUpdateCoordinator):
    """Update coordinator for Mars weather data."""

    def __init__(self, hass, api_key):
        """Initialize the data update coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="NASA Mars Weather",
            update_interval=SCAN_INTERVAL,
        )
        self.api_key = api_key

    async def _async_update_data(self):
        """Fetch data from NASA API."""
        try:
            url = "https://api.nasa.gov/insight_weather/"
            params = {
                "feedtype": "json",
                "ver": "1.0",
                "api_key": self.api_key,
            }

            # Use a session or requests library
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data or "av_t" not in data:
                raise UpdateFailed("Invalid response from NASA API")

            return data
        except requests.exceptions.RequestException as err:
            raise UpdateFailed(f"Error communicating with NASA API: {err}") from err


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the NASA Mars Weather integration."""
    api_key = entry.data.get("api_key")

    coordinator = MarsWeatherUpdateCoordinator(hass, api_key)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Register Lovelace resources for the custom card
    try:
        lovelace = hass.data.get("lovelace")
        if lovelace:
            lovelace.created_yaml_resources.add(
                "/custom_components/nasa_mars_weather/lovelace/mars-weather-card.js"
            )
    except Exception as err:
        _LOGGER.debug(f"Could not register Lovelace card: {err}")

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
