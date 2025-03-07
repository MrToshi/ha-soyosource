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
from homeassistant.exceptions import ConfigEntryNotReady

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
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://{host}/data") as resp:
                        if resp.status != 200:
                            _LOGGER.error(
                                "Error %d on %s", resp.status, host
                            )
                            return None
                        
                        # Lese die Antwort als Text und konvertiere manuell zu JSON
                        text_response = await resp.text()
                        try:
                            return json.loads(text_response)
                        except json.JSONDecodeError as err:
                            _LOGGER.error(
                                "Error decoding JSON from %s: %s - Raw response: %s",
                                host,
                                err,
                                text_response,
                            )
                            return None
        except aiohttp.ClientError as err:
            _LOGGER.error(
                "Error connecting to Soyosource Controller at %s: %s",
                host,
                err,
            )
            return None
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error(
                "Error updating Soyosource Controller at %s: %s",
                host,
                err,
            )
            return None

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="soyosource_controller",
        update_method=async_update_data,
        update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady(
            f"Failed to fetch initial data from Soyosource Controller at {host}"
        )

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
        if self.coordinator.data is None:
            return None
            
        try:
            value = self.coordinator.data.get(self._data_key)
            if value is None:
                return None
                
            # Entferne "S>" wenn vorhanden und konvertiere zu float
            if isinstance(value, str):
                value = value.strip("S>")
            return float(value)
        except (KeyError, ValueError, TypeError):
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

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data is not None 