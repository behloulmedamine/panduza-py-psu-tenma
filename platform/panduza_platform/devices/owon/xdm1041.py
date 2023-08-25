
from core.platform_device_model import PlatformDeviceModel

USBID_VENDOR="1a86"
USBID_MODEL="7523"
TTY_BASE="/dev/ttyUSB"

class DeviceOwonXdm1041(PlatformDeviceModel):
    """Multimeter From Owon
    """

    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "owon.xdm1041",
        }

    def _PZA_DEV_interfaces(self):
        """
        """
        interfaces = []

        # fake_mode = self._initial_settings.get("fake_mode", False)


        # if fake_mode:
        #     pass
        # else:
        #     interfaces.append({
        #         "name": f"bps",
        #         "driver": "hanmatek.hm310t.bps",
        #         "settings": {
        #             "usb_vendor": USBID_VENDOR,
        #             "usb_model": USBID_MODEL,
        #             "serial_baudrate": 9600
        #         }
        #     })
        #     interfaces.append({
        #         "name": f"am",
        #         "driver": "hanmatek.hm310t.ammeter",
        #         "settings": {
        #             "usb_vendor": USBID_VENDOR,
        #             "usb_model": USBID_MODEL,
        #             "serial_baudrate": 9600
        #         }
        #     })

        return interfaces

