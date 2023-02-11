# Functions called by spi_master_base for ftdi chips

from .spi_master_base import ConnectorSPIMasterBase
from loguru import logger
import pyftdi.spi as Spi
from pyftdi.ftdi import Ftdi
from pyftdi.usbtools import UsbToolsError
from .udev_tty import TTYPortFromUsbInfo
from typing import Mapping

# enum SpiPolarity
SPI_POL_RISING_FALLING = 0
SPI_POL_FALLING_RISING = 1

# enum SpiPhase
SPI_PHASE_SAMPLE_SETUP = 0
SPI_PHASE_SETUP_SAMPLE = 1

# enum SpiBitorder
SPI_BITORDER_MSB = 0
SPI_BITORDER_LSB = 1


class ConnectorSPIMasterFTDI(ConnectorSPIMasterBase) :
        """The FtdiSpi client connector
        """
        
        # Contains instances
        __instances = {}

        ###########################################################################
        ###########################################################################

        # TODO warning : Expression of type "None" cannot be assigned to parameter of type "str"
        @staticmethod
        def Get(usb_vendor_id: str = None, usb_product_id: str = None, usb_serial_id: str = None, usb_base_dev_tty: str ="/dev/ttyACM", port: str = None, frequency : float = 1E6, cs_count : int = 1, polarity: int = SPI_POL_RISING_FALLING, phase: int = SPI_PHASE_SAMPLE_SETUP, bitorder: int = SPI_BITORDER_MSB) :
                """
                Singleton main getter
                """
                log = logger.debug("********** GET FTDI SPI **********")
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
                        new_instance = ConnectorSPIMasterFTDI(port_name, usb_serial_id, port, frequency, cs_count = 1, polarity = SPI_POL_RISING_FALLING, phase = SPI_PHASE_SAMPLE_SETUP)
                        ConnectorSPIMasterFTDI.__instances[port_name] = new_instance
                except Exception as e:
                        ConnectorSPIMasterFTDI.__instances.pop(port_name)
                        raise Exception('Error during initialization').with_traceback(e.__traceback__)

                # Return the previously created
                return ConnectorSPIMasterFTDI.__instances[port_name]

        
        # TODO CS_COUNT
        # TODO apriori pas besoin des vendor et product id
        # TODO comment rendre générique ?
        # TODO bitorder: int = SPI_BITORDER_MSB ?
        def __init__(self, key: str = None, usb_serial_id: str = None, port: str = None, frequency : float = 1E6, cs_count : int = 1, polarity: int = SPI_POL_RISING_FALLING, phase: int = SPI_PHASE_SAMPLE_SETUP) :
                """Constructor
                """
                if not (key in ConnectorSPIMasterFTDI.__instances):
                        raise Exception("You need to pass through Get method to create an instance")
                else:
                        self.log = logger.bind(driver_name=key)
                        self.log.info(f"attached to the FTDI SPI Serial Connector")

                self.log.debug("********** __INIT__ CONNECTEUR FTDI SPI **********")
                # List Ftdi device URL
                # try :
                #         connected_ftdi_list = Ftdi.list_devices(f"ftdi://ftdi::{usb_serial_id}/{port}")
                # except UsbToolsError as e :
                #         raise Exception('Cannot find device').with_traceback(e.__traceback__)

                # create controller object
                # cs_count is the number of slaves
                self.spi_master = Spi.SpiController(cs_count = cs_count)

                self.spi_master.configure(f'ftdi://ftdi::{usb_serial_id}/{port}', frequency = frequency)

                # get port for SPI
                mode = (polarity << 1) | phase

                # get_port creates a port whose number is cs and its parameters are the following args
                self.spi = self.spi_master.get_port(cs = 0, freq = frequency, mode = mode)
                
                self.log.debug(f"********** ARGUMENTS {usb_serial_id} {port} {frequency} {cs_count} {polarity} {phase} {mode} **********")
                self.spi.exchange([0xca, 0xfe])
                
                # self.spi_ports = [None] * cs_count
                # for i in range(0, cs_count) :
                #         self.spi_ports[i] = self.client.get_port(cs = i, frequency = frequency[i], mode = mode[i])


                # disconnect device
                # TODO close spi
                # self.client.close(freeze = true)


        def spi_write(self, data):
                """"""
                # send dummy data to initialize connection
                self.log.debug("********** SPI WRITE CONNECTEUR **********")
                self.log.debug(f"SPI WRITE CONNECTEUR DATA {data}")
                # TODO spi est un port et non le SpiController !
                self.spi.exchange(data)

        def spi_read(self):
                """"""
                self.log.debug("********** SPI READ CONNECTEUR **********")
                self.data_read = self.spi.exchange()