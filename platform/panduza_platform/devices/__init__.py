from .ftdi          import PZA_DEVICES_LIST as FTDI_DEVICES
from .hanmatek      import PZA_DEVICES_LIST as HANMATEK_DEVICES
from .owon          import PZA_DEVICES_LIST as OWON_DEVICES
from .panduza       import PZA_DEVICES_LIST as PANDUZA_DEVICES


PZA_DEVICES_LIST = [] \
    + FTDI_DEVICES \
    + HANMATEK_DEVICES \
    + OWON_DEVICES \
    + PANDUZA_DEVICES

