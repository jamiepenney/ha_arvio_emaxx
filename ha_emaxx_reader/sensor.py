"""Support for Avio EMaxx system for Selectronic's SP Pro inverters."""
import logging

import voluptuous as vol
from arvio_emaxx_reader.arvio_emaxx_reader import ArvioEmaxxReader

from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_NAME,
)

DOMAIN = "arvio_emaxx"

_LOGGER = logging.getLogger(__name__)

ICON = "mdi:flash"
CONST_DEFAULT_HOST = "emaxx"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_IP_ADDRESS, default=CONST_DEFAULT_HOST): cv.string,
        vol.Optional(CONF_NAME, default=""): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([ArvioEmaxxSensor(
        config[CONF_IP_ADDRESS],
        "Selectronic Battery State of Charge",
        "battery_soc_percent", "%"),
        ArvioEmaxxSensor(
        config[CONF_IP_ADDRESS],
        "Selectronic Power Used",
        "power_used_watts", "W")])


class ArvioEmaxxSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, endpoint, name, type, units):
        """Initialize the sensor."""
        self._endpoint = endpoint
        self._name = name
        self._type = type
        self._state = None
        self._units = units

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._units

    async def async_update(self):
        """Get the data from the Arvio Emaxx."""
        from arvio_emaxx_reader.arvio_emaxx_reader import ArvioEmaxxReader
        self._state = await (getattr(ArvioEmaxxReader(self._endpoint), self._type)())

