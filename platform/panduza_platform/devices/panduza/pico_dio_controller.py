from ...platform_device_model import PlatformDeviceModel

USBID_VENDOR="16c0"
USBID_MODEL="05e1"

SERIAL_BAUDRATE=112500

DIO_MODBUS_ADDR=1

class DevicePanduzaPicoDioController(PlatformDeviceModel):

    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "Panduza.PicoDioController",
        }

    def _PZA_DEV_interfaces(self):
        """
        """

        # SERIAL_SHORT=E6616407E3353C27

        interfaces = []
        for id in range(0, 22):
            interfaces.append({
                "name": f"dio_{id}",
                "driver": "panduza.modbus.dio",
                "settings": {
                    "dio_id": id,
                    "usb_vendor": USBID_VENDOR,
                    "usb_model": USBID_MODEL,
                    "serial_baudrate": SERIAL_BAUDRATE,
                    "modbus_slave": 1
                }
            })

        return interfaces



