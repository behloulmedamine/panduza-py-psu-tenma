# Generic class API
# Contains generic function to call to control spi bus
# These functions wrap functions from the spi_master_ftdi

# interface

import abc

class ConnectorSPIMasterBase(metaclass=abc.ABCMeta) :
        """
        Base class for SPI master connector
        """

        @abc.abstractmethod
        def SPI_write(self, data) : # handler ?
                """
                Find connected devices
                """
                pass

        @abc.abstractmethod
        def SPI_read(self) :
                """
                Find connected devices
                """
                pass
