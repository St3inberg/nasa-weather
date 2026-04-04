"""Sensor platform for NASA Mars Weather integration."""

import logging
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfTemperature, UnitOfPressure
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry

from . import DOMAIN, MarsWeatherUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: MarsWeatherUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = [
        MarsTemperatureSensor(coordinator, "average"),
        MarsTemperatureSensor(coordinator, "min"),
        MarsTemperatureSensor(coordinator, "max"),
        MarsPressureSensor(coordinator, "average"),
        MarsPressureSensor(coordinator, "min"),
        MarsPressureSensor(coordinator, "max"),
        MarsWindSpeedSensor(coordinator, "average"),
        MarsWindSpeedSensor(coordinator, "min"),
        MarsWindSpeedSensor(coordinator, "max"),
        MarsWindDirectionSensor(coordinator),
    ]

    async_add_entities(sensors)


class MarsWeatherSensorBase(CoordinatorEntity):
    """Base class for Mars weather sensors."""

    def __init__(self, coordinator: MarsWeatherUpdateCoordinator, sensor_type: str = None):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.sensor_type = sensor_type
        self._attr_has_entity_name = True

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, "mars_weather")},
            "name": "Mars Weather",
            "manufacturer": "NASA",
        }


class MarsTemperatureSensor(MarsWeatherSensorBase):
    """Sensor for Mars temperature."""

    def __init__(self, coordinator: MarsWeatherUpdateCoordinator, sensor_type: str):
        """Initialize the sensor."""
        super().__init__(coordinator, sensor_type)
        self.sensor_type = sensor_type
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return f"mars_temp_{self.sensor_type}"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        names = {
            "average": "Temperature Average",
            "min": "Temperature Min",
            "max": "Temperature Max",
        }
        return names.get(self.sensor_type, "Temperature")

    @property
    def native_value(self) -> float:
        """Return the state."""
        if not self.coordinator.data:
            return None

        data = self.coordinator.data.get("av_t", {})
        if self.sensor_type == "average":
            return round(data.get("av"), 1) if data.get("av") is not None else None
        elif self.sensor_type == "min":
            return round(data.get("mn"), 1) if data.get("mn") is not None else None
        elif self.sensor_type == "max":
            return round(data.get("mx"), 1) if data.get("mx") is not None else None


class MarsPressureSensor(MarsWeatherSensorBase):
    """Sensor for Mars pressure."""

    def __init__(self, coordinator: MarsWeatherUpdateCoordinator, sensor_type: str):
        """Initialize the sensor."""
        super().__init__(coordinator, sensor_type)
        self.sensor_type = sensor_type
        self._attr_device_class = SensorDeviceClass.PRESSURE
        self._attr_native_unit_of_measurement = UnitOfPressure.PA

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return f"mars_pressure_{self.sensor_type}"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        names = {
            "average": "Pressure Average",
            "min": "Pressure Min",
            "max": "Pressure Max",
        }
        return names.get(self.sensor_type, "Pressure")

    @property
    def native_value(self) -> float:
        """Return the state."""
        if not self.coordinator.data:
            return None

        data = self.coordinator.data.get("av_p", {})
        if self.sensor_type == "average":
            return round(data.get("av"), 2) if data.get("av") is not None else None
        elif self.sensor_type == "min":
            return round(data.get("mn"), 2) if data.get("mn") is not None else None
        elif self.sensor_type == "max":
            return round(data.get("mx"), 2) if data.get("mx") is not None else None


class MarsWindSpeedSensor(MarsWeatherSensorBase):
    """Sensor for Mars wind speed."""

    def __init__(self, coordinator: MarsWeatherUpdateCoordinator, sensor_type: str):
        """Initialize the sensor."""
        super().__init__(coordinator, sensor_type)
        self.sensor_type = sensor_type

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return f"mars_wind_speed_{self.sensor_type}"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        names = {
            "average": "Wind Speed Average",
            "min": "Wind Speed Min",
            "max": "Wind Speed Max",
        }
        return names.get(self.sensor_type, "Wind Speed")

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return "m/s"

    @property
    def native_value(self) -> float:
        """Return the state."""
        if not self.coordinator.data:
            return None

        data = self.coordinator.data.get("av_ws", {})
        if self.sensor_type == "average":
            return round(data.get("av"), 2) if data.get("av") is not None else None
        elif self.sensor_type == "min":
            return round(data.get("mn"), 2) if data.get("mn") is not None else None
        elif self.sensor_type == "max":
            return round(data.get("mx"), 2) if data.get("mx") is not None else None


class MarsWindDirectionSensor(MarsWeatherSensorBase):
    """Sensor for Mars wind direction."""

    def __init__(self, coordinator: MarsWeatherUpdateCoordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return "mars_wind_direction"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Wind Direction"

    @property
    def native_value(self) -> str:
        """Return the state."""
        if not self.coordinator.data:
            return None

        wd_data = self.coordinator.data.get("wd", {})
        most_common = wd_data.get("most_common", {})
        return most_common.get("compass_point", "Unknown")
