"""Sensor platform for NASA Mars Weather integration."""

import logging
from dataclasses import dataclass

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPressure, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN, MarsWeatherUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# Maps measurement names to their API field key
_FIELD = {"average": "av", "min": "mn", "max": "mx"}


@dataclass
class _SensorSpec:
    data_key: str
    id_prefix: str
    display_name: str
    unit: str
    device_class: SensorDeviceClass | None
    precision: int


_SPECS = [
    _SensorSpec("av_t", "temp", "Temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 1),
    _SensorSpec("av_p", "pressure", "Pressure", UnitOfPressure.PA, SensorDeviceClass.PRESSURE, 2),
    _SensorSpec("av_ws", "wind_speed", "Wind Speed", "m/s", None, 2),
]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: MarsWeatherUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = [
        MarsMeasurementSensor(coordinator, spec, measurement)
        for spec in _SPECS
        for measurement in ("average", "min", "max")
    ] + [MarsWindDirectionSensor(coordinator)]

    async_add_entities(sensors)


class MarsWeatherSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for Mars weather sensors."""

    _attr_has_entity_name = True

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "mars_weather")},
            "name": "Mars Weather",
            "manufacturer": "NASA",
        }


class MarsMeasurementSensor(MarsWeatherSensorBase):
    """Generic sensor for any numeric Mars weather measurement."""

    def __init__(
        self,
        coordinator: MarsWeatherUpdateCoordinator,
        spec: _SensorSpec,
        measurement: str,
    ):
        super().__init__(coordinator)
        self._spec = spec
        self._measurement = measurement
        self._attr_device_class = spec.device_class
        self._attr_native_unit_of_measurement = spec.unit

    @property
    def unique_id(self) -> str:
        return f"mars_{self._spec.id_prefix}_{self._measurement}"

    @property
    def name(self) -> str:
        return f"{self._spec.display_name} {self._measurement.title()}"

    @property
    def native_value(self) -> float | None:
        if not self.coordinator.data:
            return None
        val = self.coordinator.data.get(self._spec.data_key, {}).get(_FIELD[self._measurement])
        return round(val, self._spec.precision) if val is not None else None


class MarsWindDirectionSensor(MarsWeatherSensorBase):
    """Sensor for Mars prevailing wind direction."""

    unique_id = "mars_wind_direction"
    name = "Wind Direction"

    def __init__(self, coordinator: MarsWeatherUpdateCoordinator):
        super().__init__(coordinator)

    @property
    def native_value(self) -> str | None:
        if not self.coordinator.data:
            return None
        most_common = (self.coordinator.data.get("wd") or {}).get("most_common") or {}
        return most_common.get("compass_point")
