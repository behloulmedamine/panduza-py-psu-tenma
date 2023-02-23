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
        def spi_write(self, data) :
                """
                Write data
                """
                pass

        @abc.abstractmethod
        def spi_read(self) :
                """
                Read data
                """
                pass
