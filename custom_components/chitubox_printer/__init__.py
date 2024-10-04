import asyncio
from datetime import timedelta
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.event import async_call_later
import requests

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    
    coordinator = ChituBoxPrinterCoordinator(hass, config_entry)
    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = coordinator

    await coordinator.async_config_entry_first_refresh()

    hass.config_entries.async_setup_platforms(config_entry, ["sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(config_entry, ["sensor"])

    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok

class ChituBoxPrinterCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, config_entry):
        self.host = config_entry.data["host"]
        self.port = config_entry.data["port"]

        super().__init__(
            hass,
            _LOGGER,
            name="ChituBox Printer",
            update_method=self._async_update_data,
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self):
        return await self.hass.async_add_executor_job(self.fetch_printer_status)

    def fetch_printer_status(self):
        try:
            url = f"http://{self.host}:{self.port}/api/v1/status"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            _LOGGER.error(f"Error fetching data from printer: {error}")
            return None
