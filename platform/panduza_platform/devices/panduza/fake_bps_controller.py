from core.platform_device_model import PlatformDeviceModel

import sys
class DevicePanduzaFakeBps(PlatformDeviceModel):

    def __init__(self, settings = {}) -> None:
        """Constructor
        """
        super().__init__(settings)
        
        self._number_of_channel = int( self._initial_settings.get("number_of_channel", 1) )
        
        super()._PZA_DEV_set_model("FakeBps")
        super()._PZA_DEV_set_manufacturer("Panduza")
        super()._PZA_DEV_set_characteristics({
            "number_of_channel": self._number_of_channel
        })

    def _PZA_DEV_interfaces(self):
        """
        """
        super()._PZA_DEV_interfaces()

        for chan in range(0, self._number_of_channel):
            self._interfaces.append(
                {
                    "name": f"channel_{chan}_ctrl",
                    "driver": "panduza.fake.bps_control"
                }
            )
            self._interfaces.append(
                {
                    "name": f"channel_{chan}_am",
                    "driver": "panduza.fake.ammeter",
                    "settings": {
                        "work_with_fake_bps": f"!//channel_{chan}"
                    }
                }
            )
            self._interfaces.append(
                {
                    "name": f"channel_{chan}_vl",
                    "driver": "panduza.fake.voltmeter",
                }
            )

        return self._interfaces



