import json
import threading
from dataclasses import dataclass, field
from ..core import Interface, Attribute, EnsureError, RoField, RwField

@dataclass
class Psu(Interface):
    """Interface to manage power supplies
    """
    

    interface:Interface = None
    
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

        # === STATE ===
        self.add_attribute(
            Attribute(
                name = "state"
            )
        ).add_field(
            RwField(
                name = "value"
            )
        )
        # === VOLTS ===
        self.add_attribute(
            Attribute(
                name = "volts"
            )
        ).add_field(
            RwField(
                name = "value"
            )
        )
        # === VOLTS ===
        self.add_attribute(
            Attribute(
                name = "amps"
            )
        ).add_field(
            RwField(
                name = "value"
            )
        )

        if self.ensure:
            self.ensure_init()

