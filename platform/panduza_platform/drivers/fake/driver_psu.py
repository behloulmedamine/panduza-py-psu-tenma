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


        # self._misc["model"] = "PFPS-SN42 (Panduza Fake Power Supply)"

        # self._settings["ovp"] = False
        # self._settings["ocp"] = False


        self.__fakes = {
            "state": {
                "value": "off"
            },
            "volts": {
                "goal": 0,
                "real": 0,
                "min": -1000,
                "max":  1000,
            },
            "amps": {
                "goal":  0,
                "real":  0,
                "min":   0,
                "max":  50,
            },
            # "misc": self._misc
        }

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
        return self.__fakes["state"]["value"]

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_write_state_value(self, v):
        self.log.info(f"write state : {v}")
        self.__fakes["state"]["value"] = v

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_read_volts_goal(self):
        self.log.info(f"read volts goal !")
        return self.__fakes["volts"]["goal"]

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_write_volts_goal(self, v):
        self.log.info(f"write volts : {v}")
        self.__fakes["volts"]["goal"] = v
        self.__fakes["volts"]["real"] = v
    
    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_read_volts_real(self):
        self.log.info(f"read volts real !")
        return self.__fakes["volts"]["real"]

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_read_amps_goal(self):
        self.log.info(f"read amps goal !")
        return self.__fakes["amps"]["goal"]

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_write_amps_goal(self, v):
        self.log.info(f"write amps : {v}")
        self.__fakes["amps"]["goal"] = v
        self.__fakes["amps"]["real"] = v

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_read_amps_real(self):
        self.log.info(f"read amps real !")
        return self.__fakes["amps"]["real"]

