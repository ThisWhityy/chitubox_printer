"""The __init__ file for ChituBox Printer integration."""

from .printer import Printer  # Import the Printer class

DOMAIN = "chitubox_printer"

async def async_setup(hass, config):
    """Set up the ChituBox Printer component."""
    return True
