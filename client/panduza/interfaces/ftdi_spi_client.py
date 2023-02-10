import json
import threading
from ..core import Interface, Attribute, EnsureError, RoField, RwField

from dataclasses import dataclass

@dataclass
class Ftdi_Spi(Interface):
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

		# === WRITE ===
		self.add_attribute(
			Attribute(
			name = "write"
			)
		).add_field(
			RwField(
			name = "value"
			)
		)

		# === READ ===
		self.add_attribute(
			Attribute(
			name = "read"
			)
		)
		# TODO mettre value le nb d'octet a lire ?
		# ).add_field(
		# 	RwField(
		# 	name = "value"
		# 	)
		# )