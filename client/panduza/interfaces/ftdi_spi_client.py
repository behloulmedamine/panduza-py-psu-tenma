import json
import threading
from ..core import Interface, Attribute, EnsureError, RoField, RwField

from dataclasses import dataclass

@dataclass
class Ftdi_Spi_Client(Interface):
	"""Interface to manage ftdi chip for spi
	"""

	interface : Interface = None

	def __post_init__(self):
		if self.alias:
			pass
		elif self.interface:
			# Build from an other interface
			self.alias = self.interface.alias
			self.addr = self.interface.addr
			self.port = self.interface.port
			self.topic = self.interface.topic
			self.client = self.interface.client

		super().__post_init__()

		# === CS COUNT ===
		self.add_attribute(
			Attribute(
			name = "cs_count"
			)
		).add_field(
			RwField(
				
			name = "value"
			)
		)

		# === FREQUENCY ===
		self.add_attribute(
			Attribute(
			name = "frequency"
			)
		).add_field(
			RwField(
			name = "value"
			)
		)

		# === POLARITY ===
		self.add_attribute(
			Attribute(
			name = "polarity"
			)
		).add_field(
			RwField(
			name = "value"
			)
		)

		# === PHASE ===
		self.add_attribute(
			Attribute(
			name = "phase"
			)
		).add_field(
			RwField(
			name = "value"
			)
		)
