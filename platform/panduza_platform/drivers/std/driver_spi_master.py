from ...meta_driver import MetaDriver
from ...connectors.spi_master_ftdi import ConnectorSPIMasterFTDI
from ...connectors.spi_master_aardvark import ConnectorSPIMasterAardvark
from panduza_platform.connectors.udev_tty import HuntUsbDevs

class DriverSpiMaster(MetaDriver):
        """
        Driver for drive SPI master
        """
        
        backend_dict = {
            "ftdi": ConnectorSPIMasterFTDI,
            "aardvark": ConnectorSPIMasterAardvark
        }

        ###########################################################################
        ###########################################################################

        # must match with tree.json content
        def _PZADRV_config(self):
                return {
                        "name": "GenericSPIMaster",
                        "description": "Generic Spi master interface",
                        "info": {
                                "type": "spi_master",
                                "version": "0.1"
                        },
                        "compatible": [
                                "spi_master",
                                "py.spi_master"
                        ]
                }

        ###########################################################################
        ###########################################################################

        def _PZADRV_loop_init(self, tree):
                # self.log.debug(f"{tree}")
                settings = tree["settings"]

                backend = settings.get('backend')
                
                if backend is not None:
                    self.log.info(f'using backend: {backend}')
                    connector = self.backend_dict.get(backend)
                else:
                    self.log.warning("Backend auto detection is unreliable ! Try to specify the backend for the moment")
                    #try to detect backend
                    if settings.get('unique_id') is not None or settings.get('usb_product_id') == 'e0d0':
                        backend = 'aardvark'
                    else:
                        backend = 'ftdi'
                    connector = self.backend_dict.get(backend)
                    self.log.warning(f'Auto-detect: assuming backend {backend}')
                    

                # Get the gate
                self.spi_connector = connector.Get(**settings)


                self.__cmd_handlers = {
                        "transfer" : self.__handle_cmd_transfer
                }

                self._pzadrv_init_success()

        ###########################################################################
        ###########################################################################
        
        def _PZADRV_hunt_instances(self):
            instances = []

            # 0403:6001 Future Technology Devices International, Ltd FT232 Serial (UART) IC
            # 0403:e0d0 Future Technology Devices International, Ltd Total Phase Aardvark I2C/SPI Host Adapter
            # note: also detect aardvark probe
            FTDI_UART_VENDOR="0403"
            usb_pieces = HuntUsbDevs(vendor=FTDI_UART_VENDOR, subsystem="usb")
            for p in usb_pieces:
                iss = p.get("ID_SERIAL_SHORT")
                instances.append(DriverSpiMaster.__tgen(FTDI_UART_VENDOR, p.get("ID_MODEL_ID", "DEVICE ID NOT AVAILABLE"), iss, iss))

            return instances
    
        def __tgen(vendor, model, serial_short, name_suffix):
            return {
                "name": "spi:" + name_suffix,
                "driver": "py.spi_master",
                "settings": {
                    "vendor": vendor,
                    "model": model,
                    "serial_short": serial_short
                }
            }
        
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
