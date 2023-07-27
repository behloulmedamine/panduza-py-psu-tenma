import abc
import sys

class PlatformDeviceModel:
    """Mother class for device models
    """

    def __init__(self, settings = {}) -> None:
        """Constructor
        """
        self._initial_settings = settings
        self._interfaces = []
        self._model = None
        self._manufacturer = None
        self._characteristics = {}
        self._family = None
        self.name = None

    @abc.abstractmethod
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
        
        return {
            "family": self._family,
            "model": self._model,
            "manufacturer": self._manufacturer,
            "characteristics": self._characteristics
        }

    @abc.abstractmethod
    def _PZA_DEV_interfaces(self):
        
        """
        """

    def _PZA_DEV_set_family(self, family):
        """
        """
        self._family = family

    # set model
    def _PZA_DEV_set_model(self, model):
        """
        """
        self._model = model

    def _PZA_DEV_set_name(self):
        """
        """
        self.name = self._model + "_" + self._manufacturer

    # set manufacturer
    def _PZA_DEV_set_manufacturer(self, manufacturer):
        """
        """
        self._manufacturer = manufacturer

    def _PZA_DEV_set_characteristics(self, characteristics):
        """
        """
        self._characteristics = characteristics