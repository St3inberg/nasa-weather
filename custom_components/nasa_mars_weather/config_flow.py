"""Config flow for NASA Mars Weather integration."""

import logging
import voluptuous as vol
import aiohttp
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nasa_mars_weather"


def _is_valid_mars_payload(data: dict | None) -> bool:
    """Validate payload for both legacy and latest sol-key formats."""
    if not isinstance(data, dict):
        return False

    if "av_t" in data or "av_p" in data or "av_ws" in data:
        return True

    sol_keys = data.get("sol_keys")
    if not isinstance(sol_keys, list) or not sol_keys:
        return False

    latest_sol = sorted(
        sol_keys,
        key=lambda sol: (0, int(sol)) if str(sol).isdigit() else (1, str(sol)),
    )[-1]
    sol_data = data.get(latest_sol)
    if not isinstance(sol_data, dict):
        return False

    return any(key in sol_data for key in ("AT", "PRE", "HWS", "av_t", "av_p", "av_ws"))


class NasaMarsWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow"""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Initiate a flow via user interaction."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

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
                session = async_get_clientsession(self.hass)
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status in (400, 401, 403):
                        errors["api_key"] = "invalid_api_key"
                    else:
                        response.raise_for_status()
                        data = await response.json()

                if not errors:
                    if not _is_valid_mars_payload(data):
                        errors["base"] = "invalid_response"
                    else:
                        return self.async_create_entry(title="NASA Mars Weather", data=user_input)

            except aiohttp.ClientError as err:
                errors["base"] = "cannot_connect"
            except Exception as err:
                _LOGGER.error(f"Unexpected error validating API key: {err}")
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema(
            {
                vol.Required("api_key"): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
