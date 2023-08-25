
from .drv_hanmatek_hm310t_ammeter   import DriverHM310tAmmeter
from .drv_owon_xdm1041_ammeter      import DriverXDM1041Ammeter
from .drv_panduza_fake_ammeter      import DriverFakeAmmeter


PZA_DRIVERS_LIST=[
    DriverHM310tAmmeter,
    DriverXDM1041Ammeter,
    DriverFakeAmmeter
]


