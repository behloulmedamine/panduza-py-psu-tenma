import time
from collections import ChainMap
from panduza_platform.meta_drivers.psu import MetaDriverPsu
from panduza_platform.connectors.modbus_client_serial import ConnectorModbusClientSerial

HM310T_USBID_VENDOR="1a86"
HM310T_USBID_PRODUCT="7523"
HM310T_TTY_BASE="/dev/ttyUSB"

STATE_VALUE_ENUM = { "on": 1, "off": 0 }
VOLTS_BOUNDS     = { "min": 0, "max": 30 }
AMPS_BOUNDS      = { "min": 0, "max": 10 }



def int_to_state_string(v_int):
    key_list = list(STATE_VALUE_ENUM.keys())
    val_list = list(STATE_VALUE_ENUM.values())
    position = val_list.index(v_int)
    return key_list[position]

def modbus_connector_validator(modbus_conn):
    """
    """
    res = modbus_conn.read_holding_registers(3, 1, 1)
    print("??????", res)


class DriverHM310T(MetaDriverPsu):
    """ Driver to manage the HM310T power supply
    """

    ###########################################################################
    ###########################################################################

    def _PZADRV_config(self):
        # Extend the common psu config
        return ChainMap(super()._PZADRV_config(), {
            "name": "Py_Psu_HM310T",
            "description": "Power Supply HM310T",
            "compatible": [
                "hm310t",
                "hanmatek.hm310t",
                "psu.hanmatek.hm310t",
                "py.psu.hanmatek.hm310t"
            ]
        })


    def __tgen(name_suffix):
        return {
            "name": "HM310T:" + name_suffix,
            "driver": "py.psu.hanmatek.hm310t"
        }

    def _PZADRV_tree_template(self):
        return DriverHM310T.__tgen("template")

    # def _PZADRV_hunt_instances(self):
    #     instances = []
    #     usb_pieces = HuntUsbDevs(vendor=QL355P_USBID_VENDOR, model=QL355P_USBID_MODEL, subsystem="tty")
    #     for p in usb_pieces:
    #         iss = p["ID_SERIAL_SHORT"]
    #         instances.append(DriverQL355P.__tgen(iss, iss))
    #     return instances

    ###########################################################################
    ###########################################################################

    def _PZADRV_loop_init(self, tree):

        

        # Get the gate
        self.modbus = ConnectorModbusClientSerial.Get(
            usb_vendor_id=HM310T_USBID_VENDOR,
            usb_product_id=HM310T_USBID_PRODUCT,
            usb_base_dev_tty=HM310T_TTY_BASE,
            baudrate=9600,
            validator=modbus_connector_validator
            )

        # 
        self.modbus_unit = 1

        # Constants Fields settings
        self._pzadrv_psu_update_volts_min_max(VOLTS_BOUNDS["min"], VOLTS_BOUNDS["max"])
        self._pzadrv_psu_update_amps_min_max(AMPS_BOUNDS["min"], AMPS_BOUNDS["max"])

        # Misc
        self._pzadrv_psu_update_misc("model", "HM310T (Hanmatek)")

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

    def _PZADRV_PSU_read_state_value(self):
        addr = 0x0001
        regs = self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.info(f"read state addr={hex(addr)} regs={regs}")
        str_value = int_to_state_string(regs[0])
        return str_value

    def _PZADRV_PSU_write_state_value(self, v):
        addr = 0x0001
        int16_value = STATE_VALUE_ENUM[v]
        self.log.info(f"write state addr={hex(addr)} value={int16_value}")
        self.modbus.write_register(addr, int16_value, self.modbus_unit)

    def _PZADRV_PSU_read_volts_goal(self):
        # addr = 0x0010 # not really reliable
        addr = 0x0030
        regs = self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.info(f"read volts addr={hex(addr)} regs={regs}")
        float_value = float(regs[0]) / 100.0
        return float_value

    def _PZADRV_PSU_write_volts_goal(self, v):
        addr = 0x0030
        int16_value = int(v * 100)
        self.log.info(f"write volts addr={hex(addr)} valuex100={int16_value}")
        self.modbus.write_register(addr, int16_value, self.modbus_unit)

    def _PZADRV_PSU_read_amps_goal(self):
        addr = 0x0031
        regs = self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.info(f"read amps addr={hex(addr)} regs={regs}")
        float_value = float(regs[0]) / 1000.0
        return float_value

    def _PZADRV_PSU_write_amps_goal(self, v):
        addr = 0x0031
        int16_value = int(v * 1000.0)
        self.log.info(f"write amps addr={hex(addr)} valuex1000={int16_value}")
        self.modbus.write_register(addr, int16_value, self.modbus_unit)

    ###########################################################################
    ###########################################################################

    def PZADRV_hunt():
        """
        """
        return None



