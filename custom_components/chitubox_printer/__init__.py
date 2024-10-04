"""The __init__ file for ChituBox Printer integration."""
from .const import DOMAIN
from homeassistant import config_entries

async def async_setup(hass, config):
    """Set up the ChituBox Printer component."""
    hass.data[DOMAIN] = {}
    return True
