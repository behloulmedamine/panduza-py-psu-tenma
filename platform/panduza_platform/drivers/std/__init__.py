from .driver_platform import DriverPlatform
from .driver_modbus_client import DriverModbusClient
from .driver_serial import DriverSerial
from .driver_spi_master import DriverSpiMaster

PZA_DRIVERS_LIST=[
    DriverPlatform,
    DriverModbusClient,
    DriverSerial,
    DriverSpiMaster
]
