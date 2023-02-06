import json
import threading
from ..core import Interface
from ..core import Interface, Attribute, EnsureError, RoField, RwField

from dataclasses import dataclass

@dataclass
class Ftdi_Spi_Client(Interface):
	"""Interface to manage ftdi chip for spi
	"""

	interface : Interface = None

	def __post_init__(self, alias=None, addr=None, port=None, topic=None, client=None):
		"""! Constructor
		"""
		super().__init__(alias, addr, port, topic, client)
		self._post_initialization()


	def _post_initialization(self):
		        """! Declare attributes here
			"""
			# === STATE ===
        # self.add_attribute(
        #     Attribute(
        #         name = "state"
        #     )
        # ).add_field(
        #     RwField(
        #         name = "value"
        #     )
        # )
        # # === VOLTS ===
        # self.add_attribute(
        #     Attribute(
        #         name = "volts"
        #     )
        # ).add_field(
        #     RwField(
        #         name = "value"
        #     )
        # )
        # # === VOLTS ===
        # self.add_attribute(
        #     Attribute(
        #         name = "amps"
        #     )
        # ).add_field(
        #     RwField(
        #         name = "value"
        #     )
        # )
