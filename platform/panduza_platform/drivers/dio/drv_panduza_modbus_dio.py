from hamcrest import assert_that, has_key, instance_of
from ...meta_drivers.dio import MetaDriverDio
from panduza_platform.connectors.modbus_client_serial import ConnectorModbusClientSerial

class DriverFakeDio(MetaDriverDio):

    # =============================================================================
    # FROM MetaDriverDio

    def _PZA_DRV_DIO_config(self):
        return {
            "name": "panduza.modbus.dio",
            "description": "To control DIO through the Panduza Modbus Specifications"
        }

    # ---

    async def _PZA_DRV_loop_init(self, loop, tree):
        """Init function
        Reset fake parameters
        """

        # Load settings
        assert_that(tree, has_key("settings"))
        settings = tree["settings"]
        assert_that(settings, instance_of(dict))

        # Checks
        assert_that(settings, has_key("usb_vendor"))
        assert_that(settings, has_key("usb_model"))
        assert_that(settings, has_key("serial_baudrate"))

        assert_that(settings, has_key("dio_id"))
        assert_that(settings, has_key("modbus_slave"))

        # Settings
        self.id = int(settings["dio_id"])
        self.modbus_slave = settings["modbus_slave"]
        # Get the gate connector
        self.modbus = await ConnectorModbusClientSerial.Get(**settings)

        # Call meta class
        await super()._PZA_DRV_loop_init(loop, tree)

    # ---

    async def _PZA_DRV_DIO_get_direction_value(self):
        return self.modbus.read_coil(self.id, 1, self.modbus_slave)

    # ---

    async def _PZA_DRV_DIO_set_direction_value(self, value):
        """ set value of direction value
        -  Args
            value : value to be set : in or out
        """
        if   value == "out":
            self.modbus.write_coils(self.id, True, self.modbus_slave)
        elif value == "in":
            self.modbus.write_coils(self.id, False, self.modbus_slave)
        else:
            raise Exception("error in value")

    # ---

    async def _PZA_DRV_DIO_get_direction_pull(self):
        """ get direction pull
        """
        return self.__fakes["direction"]["pull"]

    # ---

    async def _PZA_DRV_DIO_set_direction_pull(self, v):
        """ set the pull direction
        -Args
        value : value to be set : up, down or open
        """
        self.__fakes["direction"]["pull"] = v

    # ---

    async def _PZA_DRV_DIO_get_state_active(self):
        """ get the active state
        """
        return self.__fakes["state"]["active"]

    # ---

    async def _PZA_DRV_DIO_set_state_active(self,v):
        """ get the active state
        -Args
        value : value to be set : True or False
        """
        self.__fakes["state"]["active"] = v

    # ---

    async def _PZA_DRV_DIO_get_state_activeLow(self):
        """ get the active low state
        """
        return self.__fakes["state"]["active_low"]

    # ---

    async def _PZA_DRV_DIO_set_state_activeLow(self,v):
        """
        """
        self.__fakes["state"]["active_low"] = v


