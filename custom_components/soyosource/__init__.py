"""The Soyosource Controller integration."""
from __future__ import annotations

import logging
import aiohttp
import json

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

PLATFORMS: list[Platform] = [Platform.SENSOR]
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Soyosource Controller from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Überprüfe die Verbindung zum Controller
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{entry.data[CONF_HOST]}/data") as response:
                if response.status != 200:
                    raise ConfigEntryNotReady(
                        f"Error connecting to the Soyosource Controller at {entry.data[CONF_HOST]}"
                    )
                
                # Lese die Antwort als Text und konvertiere manuell zu JSON
                text_response = await response.text()
                try:
                    json_data = json.loads(text_response)
                except json.JSONDecodeError as err:
                    raise ConfigEntryNotReady(
                        f"Invalid JSON data received from the Soyosource Controller at {entry.data[CONF_HOST]}: {err}"
                    ) from err
    except aiohttp.ClientError as err:
        raise ConfigEntryNotReady(
            f"Error connecting to the Soyosource Controller at {entry.data[CONF_HOST]}: {err}"
        ) from err
    
    # Stelle sicher, dass CONF_SCAN_INTERVAL in den Daten vorhanden ist
    if CONF_SCAN_INTERVAL not in entry.data:
        data = {**entry.data, CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL}
        hass.config_entries.async_update_entry(entry, data=data)
    
    hass.data[DOMAIN][entry.entry_id] = entry.data
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok 