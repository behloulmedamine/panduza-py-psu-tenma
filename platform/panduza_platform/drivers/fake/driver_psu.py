import time
from collections import ChainMap
from ...meta_drivers.psu import MetaDriverPsu

class DriverPsuFake(MetaDriverPsu):
    """Fake PSU driver
    """

    ###########################################################################
    ###########################################################################

    def _PZADRV_config(self):
        # Extend the common psu config
        return ChainMap(super()._PZADRV_config(), {
            "name": "FakePSU",
            "description": "Virtual PSU",
            "compatible": [
                "psu.fake",
                "py.psu.fake"
            ]
        })

    ###########################################################################
    ###########################################################################

    def _PZADRV_loop_ini(self, tree):

        # Init fake values
        self.__fakes = {
            "state": {
                "value": "on"
            },
            "volts": {
                "value": 5.6
            }
        }

        # Constants Fields settings
        self._pzadrv_psu_update_volts_min_max("0", "50")

        # Misc
        self._pzadrv_psu_update_misc("model", "PFPS-SN42 (Panduza Fake Power Supply)")

        # Call meta class PSU ini
        super()._PZADRV_loop_ini(tree)

    ###########################################################################
    ###########################################################################

    def _PZADRV_loop_run(self):
        """
        """
        pass

    ###########################################################################
    ###########################################################################

    def _PZADRV_loop_err(self):
        """
        """
        pass

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_read_state_value(self):
        self.log.info(f"read state !")
        return self.__fakes["state"]["value"]

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_write_state_value(self, v):
        self.log.info(f"write state : {v}")

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_read_volts_goal(self):
        self.log.info(f"read volts !")
        return self.__fakes["volts"]["value"]

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_write_volts_goal(self, v):
        self.log.info(f"write volts : {v}")


