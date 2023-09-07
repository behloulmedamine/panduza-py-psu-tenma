
from core.platform_device import PlatformDevice

USBID_VENDOR="1a86"
USBID_MODEL="7523"
TTY_BASE="/dev/ttyUSB"

class DeviceDynamixel(PlatformDevice):
    """Servomotor
    """

    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "Dynamixel",
            "manufacturer": "Dynamixel"
        }

    def _PZA_DEV_interfaces(self):
        """
        """
        interfaces = []

        fake_mode = self._initial_settings.get("fake_mode", False)


        if fake_mode:
            pass
        else:
            interfaces.append({
                "name": f"bpc",
                "driver": "panduza.servomotor",
                "settings": {
                    "usb_vendor": USBID_VENDOR,
                    "usb_model": USBID_MODEL,
                    "serial_baudrate": 9600
                }
            })

        return interfaces

