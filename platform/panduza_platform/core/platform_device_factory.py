import traceback
from .platform_errors import InitializationError
from devices import PZA_DEVICES_LIST as INBUILT_DEVICES
import sys

class PlatformDeviceFactory:
    """Manage the factory of devices
    """

    # ---

    def __init__(self, parent_platform):
        """ Constructor
        """
        self.__devices = {}
        self.__platform = parent_platform
        self.__log = self.__platform.log

    # ---

    def produce_device(self, config):
        """Try to produce the given device model
        """
        # Get model name and control it exists in the config provided by the user
        if not "name" in config:
            raise InitializationError(f"\"name\" field is not provided in the config {config}")
        name = config["name"]

        if not name in self.__devices:
            raise InitializationError(f"\"{name}\" is not found in this platform")

        # Produce the device
        try:
            dev = self.__devices[name](config.get("settings", {}))
            self.__platform.load_interface("default", name.replace(".", "_"), {
                    "name": "device",
                    "driver": "py.device"
            }, dev)
            return dev

        except Exception as e:
            raise InitializationError(f"{traceback.format_exc()}")

    # ---

    def discover(self):
        """Find device models managers
        """
        self.__log.info(f"=")
        for dev in INBUILT_DEVICES:
            self.register_device(dev)
        self.__log.info(f"=")

    # ---

    def register_device(self, dev):
        """Register a new device
        """
        cfg = dev()._PZA_DEV_config()
        model = cfg['model']
        manufacturer = cfg['manufacturer']
        name = manufacturer + "." + model
        self.__log.info(f"Register device model {model} from {manufacturer}")
        self.__devices[name] = dev


