from core.platform_device import PlatformDevice

class DevicePanduzaFakeRelayController(PlatformDevice):

    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "FakeRelayController",
            "manufacturer": "Panduza"
        }

    def _PZA_DEV_interfaces(self):
        """
        """

        number_of_channel = int( self._initial_settings.get("number_of_channel", 1) )

        interfaces = []
        for chan in range(0, number_of_channel):
            interfaces.append(
                {
                    "name": f"channel_{chan}",
                    "driver": "panduza.fake.relay"
                }
            )

        return interfaces



