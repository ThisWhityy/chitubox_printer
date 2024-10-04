"""Sensor platform for ChituBox Printer integration."""
from homeassistant.helpers.entity import Entity
from .printer import Printer
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.helpers import config_entry

class ChituBoxPrinterSensor(Entity):
    """Representation of a ChituBox printer sensor."""

    def __init__(self, printer_ip):
        """Initialize the sensor."""
        self._printer = Printer(printer_ip)
        self._name = "ChituBox Printer Status"
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.printing_status()

    def update(self):
        """Update the sensor state."""
        self._state = self.printing_status()

    def printing_status(self):
        """Get the current printing status from the printer."""
        return self._printer.printingStatus()

    def close(self):
        """Close the printer connection."""
        self._printer.close()
