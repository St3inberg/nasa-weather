"""NASA Mars Weather Integration for Home Assistant"""

import asyncio
import logging
from datetime import timedelta

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nasa_mars_weather"
PLATFORMS = [Platform.SENSOR]
SCAN_INTERVAL = timedelta(hours=1)


def _normalize_mars_weather_payload(data: dict | None) -> dict | None:
    """Normalize NASA payload across legacy and sol-key response formats."""
    if not isinstance(data, dict):
        return None

    # Legacy format already exposes aggregated fields at top-level.
    if "av_t" in data or "av_p" in data or "av_ws" in data:
        return data

    sol_keys = data.get("sol_keys")
    if not isinstance(sol_keys, list) or not sol_keys:
        return None

    def _sol_sort_key(sol: str):
        try:
            return (0, int(sol))
        except (TypeError, ValueError):
            return (1, str(sol))

    latest_sol = sorted(sol_keys, key=_sol_sort_key)[-1]
    sol_data = data.get(latest_sol)
    if not isinstance(sol_data, dict):
        return None

    normalized = {
        "av_t": sol_data.get("AT") or sol_data.get("av_t") or {},
        "av_p": sol_data.get("PRE") or sol_data.get("av_p") or {},
        "av_ws": sol_data.get("HWS") or sol_data.get("av_ws") or {},
        "wd": sol_data.get("WD") or sol_data.get("wd") or {},
        "source_sol": latest_sol,
    }

    if not any(isinstance(normalized[key], dict) and normalized[key] for key in ("av_t", "av_p", "av_ws")):
        return None

    return normalized


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

            session = async_get_clientsession(self.hass)
            async with session.get(
                url,
                params=params,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status in (400, 401, 403):
                    raise UpdateFailed("Invalid NASA API key")
                response.raise_for_status()
                data = await response.json()

            normalized = _normalize_mars_weather_payload(data)
            if not normalized:
                raise UpdateFailed("Invalid response from NASA API")

            return normalized
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            raise UpdateFailed(f"Error communicating with NASA API: {err}") from err


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the NASA Mars Weather integration."""
    api_key = entry.data.get("api_key")

    coordinator = MarsWeatherUpdateCoordinator(hass, api_key)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
