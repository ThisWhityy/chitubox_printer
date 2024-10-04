"""Config flow for ChituBox Printer integration."""
from homeassistant import config_entries
from homeassistant.const import CONF_IP_ADDRESS, CONF_NAME
import socket

class ChituBoxPrinterConfigFlow(config_entries.ConfigFlow, domain="chitubox_printer"):
    """Handle a config flow for ChituBox Printer integration."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=self._get_data_schema())
        
        ip_address = user_input[CONF_IP_ADDRESS]
        
        # Validate the IP address
        if not self._validate_ip(ip_address):
            return self.async_show_form(
                step_id="user", 
                data_schema=self._get_data_schema(), 
                errors={"base": "invalid_ip"}
            )

        return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

    def _get_data_schema(self):
        """Return the data schema for the user step."""
        return vol.Schema({
            vol.Required(CONF_NAME, default="ChituBox Printer"): str,
            vol.Required(CONF_IP_ADDRESS): str,
        })

    def _validate_ip(self, ip):
        """Validate the IP address."""
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False
