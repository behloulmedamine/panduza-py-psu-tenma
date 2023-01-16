# Generic class API
# Contains generic function to call to control spi bus
# These functions wrap functions from the spi_master_ftdi

# interface

import abc
import aardvark_py

# hérite de metaclass ABCMeta ?
# ABC est standard

# dummy data pour lancer la clock
# detection fait par panduza

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


# TODO Questions :

# FTDI ou SPI ?
# Get ?
# TTYPortFromUsbInfo
# Interface python duck typing
# règles udev

# Liste des fonctions à implémenter ?
