"""Config flow for NASA Mars Weather integration."""

import logging
import voluptuous as vol
import requests
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nasa_mars_weather"


class NasaMarsWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow"""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Initiate a flow via user interaction."""
        errors = {}

        if user_input is not None:
            api_key = user_input["api_key"]

            # Validate the API key by making a test request
            try:
                url = "https://api.nasa.gov/insight_weather/"
                params = {
                    "feedtype": "json",
                    "ver": "1.0",
                    "api_key": api_key,
                }
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                if not data or "av_t" not in data:
                    errors["base"] = "invalid_response"
                else:
                    return self.async_create_entry(title="NASA Mars Weather", data=user_input)

            except requests.exceptions.HTTPError as err:
                if response.status_code == 400:
                    errors["api_key"] = "invalid_api_key"
                else:
                    errors["base"] = "cannot_connect"
            except requests.exceptions.RequestException:
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema(
            {
                vol.Required("api_key"): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
