from ...meta_driver import MetaDriver
from ...connectors.spi_master_ftdi import ConnectorSPIMasterFTDI

class DriverFtdiSpi(MetaDriver):
        """
        Driver for FTDI-SPI chip
        """

        ###########################################################################
        ###########################################################################

        # must match with tree.json content
        def _PZADRV_config(self):
                return {
                        "name": "FtdiSpi",
                        "description": "Generic Ftdi Spi interface",
                        "info": {
                                "type": "ftdi_spi",
                                "version": "0.1"
                        },
                        "compatible": [
                                "ftdi_spi",
                                "py_ftdi_spi"
                        ]
                }

        ###########################################################################
        ###########################################################################

        def _PZADRV_loop_init(self, tree):
                # self.log.debug(f"{tree}")
                settings = tree["settings"]


                # Get the gate
                self.spi_connector = ConnectorSPIMasterFTDI.Get(
                        usb_serial_id=settings["usb_serial_id"],
                        port=settings["port"],
                        polarity=settings["polarity"],
                        phase=settings["phase"]
                )


                self.__cmd_handlers = {
                        "transfer" : self.__handle_cmd_transfer
                }

                self._pzadrv_init_success()

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

        def __handle_cmd_transfer(self, cmd_att) :
                """
                Command handler for the write function
                Called when the user writes in the write attribute
                """
                self.log.debug(f"CMD_ATT = {cmd_att}")
                if "tx" in cmd_att:
                    values = cmd_att["tx"]
                    try:
                        # TODO give the cs to the spi write
                        read_values = self.spi_connector.spi_transfer(values)
                        self.log.debug("update")
                        self._update_attribute("transfer", "rx", list(read_values), push=True)
                    except Exception as e:
                        self.log.error(f"{e}")
