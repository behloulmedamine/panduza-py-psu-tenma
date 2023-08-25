import serial
import logging
import asyncio

from log.driver import driver_logger

from .serial_base import ConnectorSerialBase
from .udev_tty import SerialPortFromUsbSetting

class ConnectorSerialTty(ConnectorSerialBase):
    """
    """

    # Hold instances mutex
    __MUTEX = asyncio.Lock()

    # Contains instances
    __INSTANCES = {}

    # Local logs
    log = driver_logger("ConnectorSerialTty")

    ###########################################################################
    ###########################################################################

    @staticmethod
    async def Get(**kwargs):
        """Singleton main getter

        
        :Keyword Arguments:
        * *serial_port_name* (``str``) --
            serial port name
    
        * *serial_baudrate* (``int``) --
            serial
        * *serial_bytesize* (``int``) --
            serial

        * *usb_vendor* (``str``) --
            ID_VENDOR_ID
        * *usb_model* (``str``) --
            ID_MODEL_ID
        * *usb_serial_short* (``str``) --
            ID_SERIAL_SHORT

        """
        # Log
        ConnectorSerialTty.log.debug(f"Get connector for {kwargs}")

        async with ConnectorSerialTty.__MUTEX:

            # Log
            ConnectorSerialTty.log.debug(f"Lock acquired !")

            # Get the serial port name
            serial_port_name = None
            if "serial_port_name" in kwargs:
                serial_port_name = kwargs["serial_port_name"]
            elif "usb_vendor" in kwargs:
                serial_port_name = SerialPortFromUsbSetting(**kwargs)
                kwargs["serial_port_name"] = serial_port_name
            else:
                raise Exception("no way to identify the modbus serial port")

            # Create the new connector
            if not (serial_port_name in ConnectorSerialTty.__instances):
                ConnectorSerialTty.__instances[serial_port_name] = None
                # try:
                new_instance = ConnectorSerialTty(**kwargs)
                ConnectorSerialTty.__instances[serial_port_name] = new_instance
                # except Exception as e:
                #     ConnectorSerialTty.__instances.pop(serial_port_name)
                #     raise Exception('Error during initialization').with_traceback(e.__traceback__)

            # Return the previously created
            return ConnectorSerialTty.__instances[serial_port_name]


    ###########################################################################
    ###########################################################################

    def __init__(self, **kwargs):
        """Constructor
        """

        port_name = kwargs["port_name"]
        if not (port_name in ConnectorSerialTty.__instances):
            raise Exception("You need to pass through Get method to create an instance")
        else:
            self.log = logging.getLogger(port_name)
            self.log.info(f"attached to the Serial TTY Connector")

            self.__internal_driver                  = serial.serial_for_url(port_name, do_not_open=True)
            self.__internal_driver.baudrate         = 19200 if "baudrate" not in kwargs else kwargs["baudrate"]
            self.__internal_driver.bytesize         = serial.EIGHTBITS
            self.__internal_driver.parity           = serial.PARITY_NONE
            self.__internal_driver.stopbits         = serial.STOPBITS_ONE
            self.__internal_driver.rtscts           = False
            self.__internal_driver.timeout          = 10
            self.__internal_driver.write_timeout    = 10

            # Open
            self.__internal_driver.open()


    def read(self):
        pass

    def write(self, data):
        pass


    def get_internal_driver(self):
        return self.__internal_driver

