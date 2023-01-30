from .driver_platform import DriverPlatform
from .driver_modbus_client import DriverModbusClient
from .driver_serial import DriverSerial
from .driver_ftdi_spi import DriverFtdiSpi

PZA_DRIVERS_LIST=[
    DriverPlatform,
    DriverModbusClient,
    DriverSerial,
    DriverFtdiSpi
]
