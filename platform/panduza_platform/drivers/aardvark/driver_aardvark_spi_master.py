from ...meta_drivers.spi_master import MetaDriverSpiMaster
from ...connectors.spi_master_aardvark import ConnectorSPIMasterAardvark
from panduza_platform.connectors.udev_tty import HuntUsbDevs
from collections import ChainMap

class DriverAardvarkSpiMaster(MetaDriverSpiMaster):
    """
    Driver for drive SPI master
    """

    ###########################################################################
    ###########################################################################

    # must match with tree.json content
    def _PZADRV_config(self):
        # Extend the common psu config
        return ChainMap(
            super()._PZADRV_config(),
            {
                "name": "Aardvark_spi_master",
                "description": "SPI master over Aardvark chip",
                "compatible": ["Aardvark_spi_master", "py.Aardvark_spi_master"],
            },
        )

    ###########################################################################
    ###########################################################################

    def _PZADRV_loop_init(self, tree):
        # self.log.debug(f"{tree}")
        settings = tree["settings"]

        # Get the gate
        self.spi_connector = ConnectorSPIMasterAardvark.Get(**settings)
        
        super()._PZADRV_loop_init(tree)

        

    ###########################################################################
    ###########################################################################

    def _PZADRV_hunt_instances(self):
        instances = [] # ConnectorSPIMasterAardvark.hunt()

        # 0403:6001 Future Technology Devices International, Ltd FT232 Serial (UART) IC
        # 0403:e0d0 Future Technology Devices International, Ltd Total Phase Aardvark I2C/SPI Host Adapter
        # note: also detect aardvark probe
        Aardvark_UART_VENDOR = "0403"
        usb_pieces = HuntUsbDevs(vendor=Aardvark_UART_VENDOR, subsystem="usb")
        for p in usb_pieces:
            iss = p.get("ID_SERIAL_SHORT")
            instances.append(
                MetaDriverSpiMaster.__tgen(
                    "py.Aardvark_spi_master",
                    Aardvark_UART_VENDOR,
                    p.get("ID_MODEL_ID", "DEVICE ID NOT AVAILABLE"),
                    iss,
                    iss,
                )
            )

        return instances


    ###########################################################################
    ###########################################################################

    def _PZADRV_loop_run(self):
        """ """
        pass

    ###########################################################################
    ###########################################################################

    def _PZADRV_loop_err(self):
        """ """
        pass

    ###########################################################################
    ###########################################################################

    def _PZADRV_SPIM_transfer(self, data):
        return self.spi_connector.transfer(data, len(data))
