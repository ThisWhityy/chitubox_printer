import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

@config_entries.HANDLERS.register(DOMAIN)
class ChituBoxPrinterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="ChituBox Printer", data=user_input)

        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Required("port", default=80): int,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ChituBoxPrinterOptionsFlow(config_entry)


class ChituBoxPrinterOptionsFlow(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Optional("host", default=self.config_entry.data.get("host")): str,
            vol.Optional("port", default=self.config_entry.data.get("port", 80)): int,
        })

        return self.async_show_form(step_id="init", data_schema=data_schema)
