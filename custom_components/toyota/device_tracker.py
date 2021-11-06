"""Device tracker platform for Toyota Connected Services"""
import logging
from typing import Optional

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DATA_COORDINATOR, DOMAIN, IMAGE
from .entity import ToyotaBaseEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> bool:
    """Set up the device_tracker platform."""
    tracker = []

    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    for index, _ in enumerate(coordinator.data):

        vehicle = coordinator.data[index]
        if vehicle.is_connected:
            tracker.append(ToyotaParkingTracker(coordinator, index, "parking location"))

    async_add_devices(tracker, True)

    return True


class ToyotaParkingTracker(ToyotaBaseEntity, TrackerEntity):
    """Toyota Connected Services device tracker."""

    @property
    def latitude(self) -> Optional[float]:
        """Return latitude value of the device."""
        parking = self.coordinator.data[self.index].parking
        return parking.latitude if parking else None

    @property
    def longitude(self) -> Optional[float]:
        """Return longitude value of the device."""
        parking = self.coordinator.data[self.index].parking
        return parking.longitude if parking else None

    @property
    def source_type(self) -> str:
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def entity_picture(self) -> Optional[str]:
        """Return entity picture."""
        if IMAGE in self.vehicle.details:
            return self.vehicle.details[IMAGE]
        return None
