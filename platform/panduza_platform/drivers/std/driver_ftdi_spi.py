from ...meta_driver import MetaDriver
from ...connectors.spi_master_ftdi import ConnectorSPIMasterFTDI

# TODO must add a FTDI metadriver ?
# pas de metadriver pour modbus
class DriverFtdiSpi(MetaDriver):
        """
        Driver for FTDI-SPI chip
        """

        ###########################################################################
        ###########################################################################

        # must match with tree.json content
        def _PZADRV_config(self):
                return {
                        "info": {
                                "type": "ftdi_spi.client",
                                "version": "0.1"
                        },
                        "compatible": [
                                "ftdi.spi",
                                "py.ftdi.spi"
                        ]
                }

        ###########################################################################
        ###########################################################################

        def _PZADRV_loop_ini(self, tree):
                # self.log.debug(f"{tree}")

                settings = tree["settings"]


                # Get the gate
                self.ftdiSpi = ConnectorSPIMasterFTDI.Get(
                        usb_serial_id=settings["usb_serial_id"],
                        port=settings["port"],
                        polarity=settings["polarity"],
                        phase=settings["phase"],
                        bitorder=settings["bitorder"]
                )


                self.__cmd_handlers = {
                        "holding_regs": self.__handle_cmds_set_holding_regs,
                }

                self._pzadrv_ini_success()

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

        def _PZADRV_cmds_set(self, payload):
                """From MetaDriver
                """
                cmds = self.payload_to_dict(payload)
                self.log.debug(f"cmds as json : {cmds}")
                for att in self.__cmd_handlers:
                        if att in cmds:
                                self.__cmd_handlers[att](cmds[att])


        ###########################################################################
        ###########################################################################

        def __handle_cmds_set_holding_regs(self, cmd_att):
                """
                """
                if "values" in cmd_att:
                        values = cmd_att["values"]
                        try:
                                for u in values:
                                        for addr in values[u]:
                                                self.log.debug(f"on unit {u} SPI write {addr} with {values[u][addr]}")
                                                self.ftdiSpi.SPI_write(self, values) # TODO data in out ?

                                # self._update_attribute("state", "value", v)
                        except Exception as e:
                                self.log.error(f"{e}")
