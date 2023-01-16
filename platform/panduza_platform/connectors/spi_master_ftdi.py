# Functions called by spi_master_base for ftdi chips

# function Get static
# create object

from spi_master_base import ConnectorSPIMasterBase
from array import array, ArrayType # TODO ?

class ConnectorSPIMasterFTDI(ConnectorSPIMasterBase) :

        # TODO must change that
        @staticmethod
        def Get(usb_vendor_id: str = None, usb_product_id: str = None, usb_serial_id: str = None, usb_base_dev_tty: str ="/dev/ttyACM", port: str = None, baudrate: int = 19200, bytesize: int = 8, parity: chr = 'N', stopbits: int = 1, validator=None) :
                """
                Singleton main getter
                Get metadata to identify device (vendor_id, product_id ...)
                """
                pass

        # bitrate
        # polarity
        # phase
        # bitorder
        def __init__(self) : # add bitrate, polarity, phase, bitorder
                self.client = SPIMasterClient()
                # constructor ?
                

        def SPI_write(self, data_in, data_out):
                """"""
                # send dummy data to initialize connection
                self
                return

        def SPI_read(self):
                return 
