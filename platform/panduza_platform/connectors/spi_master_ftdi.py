# Functions called by spi_master_base for ftdi chips

from .spi_master_base import ConnectorSPIMasterBase
from loguru import logger
import pyftdi.spi as Spi
from pyftdi.ftdi import Ftdi
from pyftdi.usbtools import UsbToolsError
from .udev_tty import TTYPortFromUsbInfo

from spi_master_base import ConnectorSPIMasterBase
from array import array, ArrayType # TODO ?

class ConnectorSPIMasterFTDI(ConnectorSPIMasterBase) :
        """The FtdiSpi client connector
        """
        
        # Contains instances
        __instances = {}

        ###########################################################################
        ###########################################################################

        # TODO warning : Expression of type "None" cannot be assigned to parameter of type "str"
        @staticmethod
        def Get(usb_vendor_id: str = None, usb_product_id: str = None, usb_serial_id: str = None, usb_base_dev_tty: str ="/dev/ttyACM", port: str = None, polarity: int = SPI_POL_RISING_FALLING, phase: int = SPI_PHASE_SAMPLE_SETUP, bitorder: int = SPI_BITORDER_MSB) :
                """
                Singleton main getter
                Get metadata to identify device (vendor_id, product_id ...)
                """
                port_name = ""
                if port != "":
                        port_name = port
                elif usb_vendor_id != None and usb_product_id != None:
                        port_name = TTYPortFromUsbInfo(usb_vendor_id, usb_product_id, usb_serial_id, usb_base_dev_tty)
                else:
                        raise Exception("no way to identify the SPI serial port")

                # Create the new connector
                if not (port_name in ConnectorSPIMasterFTDI.__instances):
                        ConnectorSPIMasterFTDI.__instances[port_name] = None
                try:
                        new_instance = ConnectorSPIMasterFTDI(port_name, usb_serial_id, port)
                        ConnectorSPIMasterFTDI.__instances[port_name] = new_instance
                except Exception as e:
                        ConnectorSPIMasterFTDI.__instances.pop(port_name)
                        raise Exception('Error during initialization').with_traceback(e.__traceback__)

                # Return the previously created
                return ConnectorSPIMasterFTDI.__instances[port_name]


        # TODO warning : Expression of type "None" cannot be assigned to parameter of type "str"
        # TODO apriori pas besoin des vendor et product id
        def __init__(self, key: str = None, usb_serial_id: str = None, port: str = None, polarity: int = SPI_POL_RISING_FALLING, phase: int = SPI_PHASE_SAMPLE_SETUP, bitorder: int = SPI_BITORDER_MSB) :
                """Constructor
                """
                if not (key in ConnectorSPIMasterFTDI.__instances):
                        raise Exception("You need to pass through Get method to create an instance")
                else:
                        self.log = logger.bind(driver_name=key)
                        self.log.info(f"attached to the FTDI SPI Serial Client Connector")

                # List Ftdi device URL
                # try :
                #         connected_ftdi_list = Ftdi.list_devices(f"ftdi://ftdi::{usb_serial_id}/{port}")
                # except UsbToolsError as e :
                #         raise Exception('Cannot find device').with_traceback(e.__traceback__)

                # create client object
                self.client = Spi.SpiController() # TODO est ce que je donne les args du constructor ?
                self.client.configure(f'ftdi://ftdi::{usb_serial_id}/{port}')
                # self.client.configure(f'ftdi://ftdi::FT8CEM8A/2')

                # get port for SPI
                self.spi = self.client.get_port(cs = 0, freq = 1E6, mode = 0)

                # disconnect device
                # client.close(freeze = True)


        def SPI_write(self, data):
                """"""
                # send dummy data to initialize connection
                self.spi.exchange(data)

        def SPI_read(self):
                """"""
                return self.spi.exchange()
