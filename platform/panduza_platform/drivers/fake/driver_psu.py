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

    def _PZADRV_loop_init(self, tree):

        # Init fake values
        self._state["value"] = "off"

        self._volts["goal"] = 0
        self._volts["real"] = 0
        self._volts["min"] = -1000
        self._volts["max"] = 1000

        self._amps["goal"] = 0
        self._amps["real"] = 0
        self._amps["min"] = 0
        self._amps["max"] = 50

        self._misc["model"] = "PFPS-SN42 (Panduza Fake Power Supply)"

        self._settings["ovp"] = False
        self._settings["ocp"] = False

        self.__fakes = {
            "state": self._state,
            "volts": self._volts,
            "amps": self._amps,
            "misc": self._misc
        }

        # Constants Fields settings
        self._update_attributes_from_dict(self.__fakes)

        # Call meta class PSU ini
        super()._PZADRV_loop_init(tree)

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
        return self._state["value"]

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_write_state_value(self, v):
        self.log.info(f"write state : {v}")
        self._state["value"] = v

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_read_volts_goal(self):
        self.log.info(f"read volts goal !")
        return self._volts["goal"]

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_write_volts_goal(self, v):
        self.log.info(f"write volts : {v}")
        self._volts["goal"] = v
        self._volts["real"] = v
    
    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_read_volts_real(self):
        self.log.info(f"read volts real !")
        return self._volts["real"]