from hamcrest import assert_that, has_key, instance_of
from meta_drivers.bpc import MetaDriverBpc
from connectors.modbus_client_serial import ConnectorModbusClientSerial

STATE_VALUE_ENUM = { True : 1, False: 0  }
VOLTAGE_BOUNDS     = { "min": 0, "max": 30 }
CURRENT_BOUNDS      = { "min": 0, "max": 10 }

def int_to_state_string(v_int):
    key_list = list(STATE_VALUE_ENUM.keys())
    val_list = list(STATE_VALUE_ENUM.values())
    position = val_list.index(v_int)
    return key_list[position]

class DrvHanmatekHm310tBpc(MetaDriverBpc):
    """ Driver to manage the HM310T power supply
    """

    # =============================================================================
    # FROM MetaDriverBpc

    # ---

    def _PZA_DRV_BPC_config(self):
        """
        """
        return {
            "name": "hanmatek.hm310t.bpc",
            "description": "Power Supply HM310T from Hanmatek"
        }

    # ---

    async def _PZA_DRV_loop_init(self, loop, tree):
        """Driver initialization
        """

        # Load settings
        assert_that(tree, has_key("settings"))
        settings = tree["settings"]
        assert_that(settings, instance_of(dict))

        # Checks
        assert_that(settings, has_key("usb_vendor"))
        assert_that(settings, has_key("usb_model"))
        assert_that(settings, has_key("serial_baudrate"))

        # Get the gate
        self.modbus = await ConnectorModbusClientSerial.Get(**settings)

        # 
        self.modbus_unit = 1

        # Call meta class BPC ini
        await super()._PZA_DRV_loop_init(loop, tree)

    ###########################################################################
    ###########################################################################

    # STATE #

    async def _PZA_DRV_BPC_read_enable_value(self):
        addr = 0x0001
        regs = await self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.debug(f"read state addr={hex(addr)} regs={regs}")
        str_value = int_to_state_string(regs[0])
        return str_value

    # ---

    async def _PZA_DRV_BPC_write_enable_value(self, v):
        addr = 0x0001
        int16_value = STATE_VALUE_ENUM[v]
        self.log.info(f"write state addr={hex(addr)} value={int16_value}")
        await self.modbus.write_register(addr, int16_value, self.modbus_unit)

    # VOLTAGE #

    async def _PZA_DRV_BPC_read_voltage_value(self):
        addr = 0x0030
        regs = await self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.debug(f"read value voltage addr={hex(addr)} regs={regs}")
        float_value = float(regs[0]) / 100.0
        return float_value

    # ---

    async def _PZA_DRV_BPC_write_voltage_value(self, v):
        addr = 0x0030
        int16_value = int(v * 100)
        self.log.info(f"write value voltage addr={hex(addr)} valuex100={int16_value}")
        await self.modbus.write_register(addr, int16_value, self.modbus_unit)

    # ---

    async def _PZA_DRV_BPC_voltage_value_min_max(self):
        return VOLTAGE_BOUNDS

    # ---

    async def _PZA_DRV_BPC_read_voltage_decimals(self):
        return 2

    # CURRENT #

    async def _PZA_DRV_BPC_read_current_value(self):
        addr = 0x0031
        regs = await self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.debug(f"read value current addr={hex(addr)} regs={regs}")
        float_value = float(regs[0]) / 1000.0
        return float_value

    # ---

    async def _PZA_DRV_BPC_write_current_value(self, v):
        addr = 0x0031
        int16_value = int(v * 1000.0)
        self.log.info(f"write value current addr={hex(addr)} valuex1000={int16_value}")
        await self.modbus.write_register(addr, int16_value, self.modbus_unit)

    # ---

    async def _PZA_DRV_BPC_current_value_min_max(self):
        return CURRENT_BOUNDS

    # ---

    async def _PZA_DRV_BPC_read_current_decimals(self):
        return 3

