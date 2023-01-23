# Functions called by spi_master_base for ftdi chips

# function Get static
# create object

from spi_master_base import ConnectorSPIMasterBase
from loguru import logger
import pyftdi.spi as Spi
import aardvark_py as AA # TODO à suppr

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

        @staticmethod
        def Get(port: str = "", polarity: int = SPI_POL_RISING_FALLING, phase: int = SPI_PHASE_SAMPLE_SETUP, bitorder: int = SPI_BITORDER_MSB) :
                """
                Singleton main getter
                """
                # Get the serial port key
                # TODO est ce que j'ai besoin de usb vendor id etc ... ?
                # TTYPortFromUsbInfo ?
                # la carte est relié en USB
                # pour discriminer la carte, j'ai besoin de vendor id et du serial number ?
                # il est dans settings ?
                port_name = ""
                if port != "":
                        port_name = port

                else:
                        raise Exception("no way to identify the modbus serial port")

                # Create the new connector
                if not (port_name in ConnectorSPIMasterFTDI.__instances):
                        ConnectorSPIMasterFTDI.__instances[port_name] = None
                try:
                        new_instance = ConnectorSPIMasterFTDI(port_name, polarity, phase, bitorder)
                        ConnectorSPIMasterFTDI.__instances[port_name] = new_instance
                except Exception as e:
                        ConnectorSPIMasterFTDI.__instances.pop(port_name)
                        raise Exception('Error during initialization').with_traceback(e.__traceback__)

                # Return the previously created
                return ConnectorSPIMasterFTDI.__instances[port_name]



        def __init__(self, key: str = "", polarity: int = SPI_POL_RISING_FALLING, phase: int = SPI_PHASE_SAMPLE_SETUP, bitorder: int = SPI_BITORDER_MSB) : 
                """Constructor
                """
                if not (key in ConnectorSPIMasterFTDI.__instances):
                        raise Exception("You need to pass through Get method to create an instance")
                else:
                        self.log = logger.bind(driver_name=key)
                        self.log.info(f"attached to the Modbus Serial Client Connector")

                # create client object
                self.client = Spi.SpiController() # TODO est ce que je donne les args du constructor ?
                self.client.configure('ftdi://ftdi:2232:FT7TS7JR/1') # TODO où je donne le numéro de série ? Dans les param ?
                # TODO dans configure, dans l'url, ou est port name ?
                # ftdi://ftdi:2232:FT7TS7JR/1
                # (f'ftdi://{chip_number}{serial_number}{port_name}')
                # TTYPortFromUsbInfo ?

                # connect to device
                # self.client.connect()
                # TODO connect ? la connexion mqtt se fait dans le metal

                # TODO est ce que les arg ici ne sont pas ceux à donner dans init ?
                # spi = self.client.get_port(cs = 0, freq = 1E6, mode = 0) 

                # TODO write ?

                # disconnect device
                # client.close(freeze = True)


        def SPI_write(self, data_in, data_out):
                """"""
                # send dummy data to initialize connection
                # AA.aa_spi_write()
                return

        def SPI_read(self):
                # AA.aa_spi_slave_read()
                return 