import abc
import sys
import traceback
from .platform_worker import PlatformWorker

class PlatformDeviceModel:
    """Mother class for device models
    """

    def __init__(self, settings = {}) -> None:
        """Constructor
        """
        self._initial_settings = settings
        self._interfaces = []
        self._interfaces_obj = []
        self._model = None
        self._manufacturer = None
        self._characteristics = {}
        self._family = None
        self.name = None

    def _PZA_DEV_config(self):
        """
        """
        if self._family == None:
            raise Exception("Family is not set")
        if self._model == None:
            raise Exception("Model is not set")
        if self._manufacturer == None:
            raise Exception("Manufacturer is not set")
        if self._characteristics == None:
            raise Warning("Characteristics is not set")
        self._PZA_DEV_set_name()
        self._PZA_DEV_create_interfaces()
        return {
            "family": self._family,
            "model": self._model,
            "manufacturer": self._manufacturer,
            "characteristics": self._characteristics
        }

    def _PZA_DEV_create_interfaces(self):
        
        """
        """
        self._interfaces.append({
                "name": "device",
                "driver": "py.device",
        })
    
    def _PZA_DEV_interfaces(self):
        """
        """
        return self._interfaces

    def _PZA_DEV_interface_objs(self):
        """
        """
        return self._interfaces_obj

    def _PZA_DEV_set_family(self, family):
        """
        """
        self._family = family

    def _PZA_DEV_set_model(self, model):
        """
        """
        self._model = model

    def _PZA_DEV_set_name(self):
        """
        """
        self.name = self._model + "_" + self._manufacturer

    def _PZA_DEV_set_manufacturer(self, manufacturer):
        """
        """
        self._manufacturer = manufacturer

    def _PZA_DEV_set_characteristics(self, characteristics):
        """
        """
        self._characteristics = characteristics

    def _PZA_DEV_create_united_interfaces(self, name, start, len, list_of_interfaces):
        """
        """
        for i in range(start, start + len):
            for key, value in list_of_interfaces.items():
                if not isinstance(value, dict):
                    raise Exception("United interface value is not a dict")
                if "driver" not in value:
                    raise Exception("United interface value does not have interface key")
                self._interfaces.append({
                    "name": ":" + name + "_" + str(i) + ":" + key,
                    "driver": value["driver"],
                    "settings": value.get("settings", {})
                })

    def append_device_interface(self, interface):
        """
        """
        self._interfaces.append(interface)

    def add_interface_obj(self, interface):
        """
        """
        self._interfaces_obj.append(interface)

    def number_of_interfaces(self):
        """
        """
        return len(self._interfaces)