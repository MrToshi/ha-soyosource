"""Support for Soyosource Controller sensors."""
from __future__ import annotations

import logging
from datetime import timedelta
import aiohttp
import async_timeout
import json

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    CONF_HOST,
    UnitOfPower,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    SENSOR_L1L2L3,
    SENSOR_CONTROLLER_NAME,
    SENSOR_START_TIME,
    SENSOR_NOT_AUS,
    SENSOR_WAIT_SEKUNDEN,
    SENSOR_MAX_POWER,
    SENSOR_SOYO_COUNT,
    SENSOR_DC_AMPS,
    SENSOR_DC_VOLTS,
    SENSOR_DC_WATTS,
    SENSOR_WATTS_OUT,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigType,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Soyosource Controller sensors."""
    host = config_entry.data[CONF_HOST]

    async def async_update_data():
        """Fetch data from API endpoint."""
        async with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{host}/data") as resp:
                    return await resp.json()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="soyosource_controller",
        update_method=async_update_data,
        update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    sensors = [
        SoyosourceSensor(
            coordinator,
            SENSOR_L1L2L3,
            "L1L2L3",
            "L1L2L3",
            SensorDeviceClass.POWER,
            UnitOfPower.WATT,
        ),
        SoyosourceSensor(
            coordinator,
            SENSOR_MAX_POWER,
            "Max Power",
            "MaxPower",
            SensorDeviceClass.POWER,
            UnitOfPower.WATT,
        ),
        SoyosourceSensor(
            coordinator,
            SENSOR_DC_AMPS,
            "DC Ampere",
            "DCAmps",
            SensorDeviceClass.CURRENT,
            UnitOfElectricCurrent.AMPERE,
        ),
        SoyosourceSensor(
            coordinator,
            SENSOR_DC_VOLTS,
            "DC Volt",
            "DCVolts",
            SensorDeviceClass.VOLTAGE,
            UnitOfElectricPotential.VOLT,
        ),
        SoyosourceSensor(
            coordinator,
            SENSOR_DC_WATTS,
            "DC Watt",
            "DCWatts",
            SensorDeviceClass.POWER,
            UnitOfPower.WATT,
        ),
        SoyosourceSensor(
            coordinator,
            SENSOR_WATTS_OUT,
            "Watts Out",
            "WattsOut",
            SensorDeviceClass.POWER,
            UnitOfPower.WATT,
        ),
    ]

    async_add_entities(sensors)


class SoyosourceSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Soyosource sensor."""

    def __init__(
        self,
        coordinator,
        sensor_type,
        name,
        data_key,
        device_class=None,
        unit_of_measurement=None,
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._name = name
        self._data_key = data_key
        self._device_class = device_class
        self._unit_of_measurement = unit_of_measurement
        self._attr_unique_id = f"{DOMAIN}_{sensor_type}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Soyosource {self._name}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        try:
            return float(self.coordinator.data[self._data_key].strip("S>"))
        except (KeyError, ValueError):
            return None

    @property
    def device_class(self):
        """Return the device class."""
        return self._device_class

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def state_class(self):
        """Return the state class."""
        return SensorStateClass.MEASUREMENT 