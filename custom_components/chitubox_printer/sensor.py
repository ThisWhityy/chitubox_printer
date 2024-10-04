from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up ChituBox printer sensor."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([ChituBoxPrinterSensor(coordinator)])


class ChituBoxPrinterSensor(Entity):
    """Representation of a ChituBox printer sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator

    @property
    def name(self):
        """Return the name of the sensor."""
        return "ChituBox Printer"

    @property
    def state(self):
        """Return the state of the sensor."""
        data = self.coordinator.data
        if data:
            return data.get("status")
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self.coordinator.data
        if data:
            return {
                "progress": data.get("progress"),
                "temperature": data.get("temperature"),
                "file_name": data.get("file_name"),
            }
        return {}

    def update(self):
        """Update the sensor."""
        self.coordinator.async_request_refresh()
