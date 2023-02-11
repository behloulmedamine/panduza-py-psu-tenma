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

        def _PZADRV_loop_ini(self, tree):
                # self.log.debug(f"{tree}")
                self.log.debug("********** _PZADRV_loop_ini FTDI SPI **********")
                settings = tree["settings"]


                # Get the gate
                self.ftdiSpi = ConnectorSPIMasterFTDI.Get(
                        usb_serial_id=settings["usb_serial_id"],
                        port=settings["port"],
                        polarity=settings["polarity"],
                        phase=settings["phase"]
                        # bitorder=settings["bitorder"] TODO
                )


                self.__cmd_handlers = {
                        "write" : self.__handle_cmd_write,
                        "read" : self.__handle_cmd_read
                }

                # self._update_attribute("phase") TODO
                # self._update_attribute("")

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

        # TODO c'est probablement pas bon write read
        # TODO que faire avec les data ?
        # def _PZADRV_SPI_read(self) :
        #         return self.ftdiSpi.spi_read()

        # def _PZADRV_SPI_write(self, data) :
        #         self.ftdiSpi.spi_write(data)

        def __handle_cmd_write(self, cmd_att) :
                """
                """
                self.log.debug("********** __HANDLE_CMD_WRITE **********")
                self.log.debug(f"CMD_ATT = {cmd_att}")
                if "values" in cmd_att:
                        self.log.debug("********** 1111111111111111111 **********")
                        values = cmd_att["values"]
                        try:
                                self.log.debug("********** 222222222222 **********")
                                self.log.debug(f"spi write data {values} type : {type(values[1])}")
                                self.ftdiSpi.spi_write(values)
                                # TODO give the cs the spi write
                                # self._update_attribute("state", "value", v)
                        except Exception as e:
                                self.log.debug("********** 333333333333 **********")
                                self.log.error(f"{e}")

        #TODO FAIRE READ
        def __handle_cmd_read(self) :
                """
                """
                try:
                        self.log.debug(f"spi read data ")
                        self.ftdiSpi.spi_read()
                except Exception as e:
                        self.log.error(f"{e}")