from core.platform_device_model import PlatformDeviceModel

import sys
class DevicePanduzaFakeBps(PlatformDeviceModel):

    def __init__(self, settings = {}) -> None:
        """Constructor
        """
        super().__init__(settings)
        
        self._number_of_channel = int( self._initial_settings.get("number_of_channel", 1) )
        
        super()._PZA_DEV_set_family("bps")
        super()._PZA_DEV_set_model("FakeBps")
        super()._PZA_DEV_set_manufacturer("Panduza")
        super()._PZA_DEV_set_characteristics({
            "number_of_channel": self._number_of_channel
        })

    def _PZA_DEV_create_interfaces(self):
        """
        """
        super()._PZA_DEV_create_interfaces()
        super()._PZA_DEV_create_united_interfaces(
            "channel", 0, self._number_of_channel,
            {
                "ctrl": {
                    "driver": "panduza.fake.bps_control",
                    "settings": {
                        "test": "tset"
                    }
                },
                "am": {
                    "driver": "panduza.fake.ammeter"
                },
                "vm": {
                    "driver": "panduza.fake.voltmeter"
                }
            }
        )
