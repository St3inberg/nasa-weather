"""Updates for NASA Mars Weather integration to support Lovelace card"""

import logging
from homeassistant.helpers.entity_registry import async_get

_LOGGER = logging.getLogger(__name__)

CARD_VERSION = "1.0.0"


async def async_setup_entry_with_card(hass):
    """Add Lovelace card to the integration"""
    try:
        # Frontend resources for custom card
        await hass.data.get("lovelace").load_resources(
            resources=[
                {
                    "url": "/custom_components/nasa_mars_weather/lovelace/mars-weather-card.js",
                    "type": "module",
                }
            ]
        )
    except Exception as e:
        _LOGGER.warning(f"Could not load Lovelace card: {e}")
