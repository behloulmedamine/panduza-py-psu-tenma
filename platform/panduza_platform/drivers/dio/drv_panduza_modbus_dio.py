from hamcrest import assert_that, has_key, instance_of
from ...meta_drivers.dio import MetaDriverDio
from panduza_platform.connectors.modbus_client_serial import ConnectorModbusClientSerial

DIO_OFFSET_PULLS = 32
DIO_OFFSET_WRITE = 64

class DriverPanduzaModbusDio(MetaDriverDio):

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
        self.activeLow = False
        # Get the gate connector
        self.modbus = await ConnectorModbusClientSerial.Get(**settings)

        # Call meta class
        await super()._PZA_DRV_loop_init(loop, tree)

    # ---

    async def _PZA_DRV_DIO_get_direction_value(self):
        
        
        coils = await self.modbus.read_coils(self.id, 1, self.modbus_slave)
        
        self.log.debug(f"{self.id} coills {coils}")
        
        return coils

    # ---

    async def _PZA_DRV_DIO_set_direction_value(self, value):
        """ set value of direction value
        -  Args
            value : value to be set : in or out
        """
        register_data = None
        if   value == "out":
            register_data = True
        elif value == "in":
            register_data = False
        else:
            raise Exception(f"Error invalid value {value}")
        await self.modbus.write_coils(self.id, register_data, self.modbus_slave)

    # ---

    async def _PZA_DRV_DIO_get_direction_pull(self):
        """ get direction pull
        """
        return await self.modbus.read_coils(DIO_OFFSET_PULLS + self.id, 1, self.modbus_slave)

    # ---

    async def _PZA_DRV_DIO_set_direction_pull(self, value):
        """ set the pull direction
        -Args
        value : value to be set : up, down or open
        """
        register_data = None
        if value == "up":
            register_data = True
        elif value == "down":
            register_data = False
        else:
            raise Exception(f"Error invalid value {value}")
        await self.modbus.write_coils(DIO_OFFSET_PULLS + self.id, register_data, self.modbus_slave)

    # ---

    async def _PZA_DRV_DIO_get_state_active(self):
        return await self.modbus.read_discrete_inputs(self.id+1, 1, self.modbus_slave)

    # ---

    async def _PZA_DRV_DIO_set_state_active(self, v):
        cmd_value = v
        if self.activeLow:
            if v:
                cmd_value = False
            else:
                cmd_value = True
        await self.modbus.write_coil(DIO_OFFSET_WRITE + self.id, cmd_value, self.modbus_slave)

    # ---

    async def _PZA_DRV_DIO_get_state_activeLow(self):
        return self.activeLow

    # ---

    async def _PZA_DRV_DIO_set_state_activeLow(self, v):
        self.activeLow = v


