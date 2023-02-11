from ..meta_driver import MetaDriver


class MetaDriverPsu(MetaDriver):
    """ Abstract Driver with helper class to manage power supply interface
    """

    ###########################################################################
    ###########################################################################
    #
    # Data and variables
    #
    ###########################################################################
    ###########################################################################

    _state = {
        "value": "off"
    }

    _volts = {
        "goal": 0,
        "real": 0,
        "min": 0,
        "max": 0
    }

    _amps = {
        "goal": 0,
        "real": 0,
        "min": 0,
        "max": 0
    }

    _misc = {
        "model": "",
        "serial": ""
    }

    _settings = {
        "ovp": False,
        "ocp": False,
    }

    ###########################################################################
    ###########################################################################
    #
    # TO OVERRIDE IN DRIVER
    #
    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_read_state_value(self):
        """Must get the state value on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_write_state_value(self, v):
        """Must set *v* as the new state value on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    # ---

    def _PZADRV_PSU_read_volts_goal(self):
        """Must get the volts goal value on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_write_volts_goal(self, v):
        """Must set *v* as the new volts goal value on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_read_volts_real(self):
        """Must get the volts real value on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    # ---

    def _PZADRV_PSU_read_amps_goal(self):
        """Must get the volts goal value on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_write_amps_goal(self, v):
        """Must set *v* as the new volts goal value on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_read_amps_real(self):
        """Must get the volts real value on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    # ---

    def _PZADRV_PSU_settings_capabilities(self):
        """Must return the psu settings capabilities in the given object
        """
        raise {
            "ovp": False,       # Over Voltage Protection
            "ocp": False,       # Over Current Protection
            "silent": False,    # Silent mode
        }

    def _PZADRV_PSU_read_settings_ovp(self):
        """Must get the ovp state on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_write_settings_ovp(self, v):
        """Must set *v* as the new ovp state on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_read_settings_ocp(self):
        """Must get the ocp state on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_write_settings_ocp(self, v):
        """Must set *v* as the new ocp state on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_read_settings_silent(self):
        """Must get the silent state on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_write_settings_silent(self, v):
        """Must set *v* as the new silent state on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    ###########################################################################
    ###########################################################################
    #
    # FOR SUBCLASS USE ONLY
    #
    ###########################################################################
    ###########################################################################

    def _pzadrv_psu_update_volts_min_max(self, min, max):
        self._update_attribute("volts", "min", min, False)
        self._update_attribute("volts", "max", max)

    # ---

    def _pzadrv_psu_update_amps_min_max(self, min, max):
        self._update_attribute("amps", "min", min, False)
        self._update_attribute("amps", "max", max)

    # ---

    def _pzadrv_psu_update_misc(self, field, value):
        self._update_attribute("misc", field, value)

    ###########################################################################
    ###########################################################################
    #
    # MATA DRIVER OVERRIDE
    #
    ###########################################################################
    ###########################################################################

    def _PZADRV_config(self):
        """Driver base configuration
        """
        return {
            "info": {
                "type": "psu",
                "version": "1.0"
            },
        }

    # ---

    def _PZADRV_loop_init(self, tree):

        self.__cmd_handlers = {
            "state": self.__handle_cmds_set_state,
            "volts": self.__handle_cmds_set_volts,
            "amps": self.__handle_cmds_set_amps,
            "settings": self.__handle_cmds_set_settings
        }

        self._pzadrv_init_success()

    # ---

    def _PZADRV_loop_run(self):
        pass

    # ---

    def _PZADRV_cmds_set(self, payload):
        """From MetaDriver
        """
        cmds = self.payload_to_dict(payload)
        # self.log.debug(f"cmds as json : {cmds}")
        for att in self.__cmd_handlers:
            if att in cmds:
                self.__cmd_handlers[att](cmds[att])

    ###########################################################################
    ###########################################################################
    #
    # PRIVATE
    #
    ###########################################################################
    ###########################################################################

    def __handle_cmds_set_state(self, cmd_att):
        """
        """
        if "value" in cmd_att:
            v = cmd_att["value"]
            # if not isinstance(v, int) or not isinstance(v, float):
            #     raise Exception(f"Invalid type for volts.value {type(v)}")
            try:
                self._PZADRV_PSU_write_state_value(v)
                self._update_attribute("state", "value", v)
            except Exception as e:
                self.log.error(f"{e}")

    # ---

    def __handle_cmds_set_volts(self, cmd_att):
        """
        """
        if "goal" in cmd_att:
            v = cmd_att["goal"]
            if not isinstance(v, int) and not isinstance(v, float):
                raise Exception(f"Invalid type for volts.goal {type(v)}")
            try:
                if self._get_field("volts", "min") <= v <= self._get_field("volts", "max"):
                    self._PZADRV_PSU_write_volts_goal(v)
                    self._update_attributes_from_dict(
                    {
                        "volts": {
                            "goal": self._PZADRV_PSU_read_volts_goal(),
                            "real": self._PZADRV_PSU_read_volts_real()
                        }
                    })
                    #self._update_attribute(
                    #    "volts", "goal", self._PZADRV_PSU_read_volts_goal())
                else:
                    self.log.error(
                        f"goal {v} out of range {self._get_field('volts', 'min')} < {self._get_field('volts', 'max')}")
            except Exception as e:
                self.log.error(f"{e}")

    # ---

    def __handle_cmds_set_amps(self, cmd_att):
        """
        """
        if "goal" in cmd_att:
            v = cmd_att["goal"]
            if not isinstance(v, int) and not isinstance(v, float):
                raise Exception(f"Invalid type for volts.goal {type(v)}")
            try:
                self._PZADRV_PSU_write_amps_goal(v)
                self._update_attribute("amps", "goal", v)
            except Exception as e:
                self.log.error(f"{e}")

    # ---

    def __handle_cmds_set_settings(self, cmd_att):
        if "ovp" in cmd_att:
            v = cmd_att["ovp"]


