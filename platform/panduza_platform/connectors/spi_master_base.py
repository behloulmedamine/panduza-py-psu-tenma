# Generic class API
# Contains generic function to call to control spi bus
# These functions wrap functions from the spi_master_ftdi

# interface

import abc
# udevadm info /dev/ttyUSB0

# hérite de metaclass ABCMeta
# ABC est standard

# dummy data pour lancer la clock
# detection faite par panduza

class ConnectorSPIMasterBase(metaclass=abc.ABCMeta) :
        """
        Base class for SPI master connector
        """

        @abc.abstractmethod
        def SPI_write(self, data) :
                """
                Write data (MOSI)
                """
                pass

        @abc.abstractmethod
        def SPI_read(self) :
                """
                Read data (MISO)
                """
                pass

# TODO Must change argument