import os
import json
import logging
import threading

from abc import ABC, abstractmethod
from typing      import Optional, Callable, Set
from dataclasses import dataclass, field

from .client import Client


from .attribute import Attribute


# -----------------------------------------------------------------------------

@dataclass
class Field:
    # Name of the field
    name: str
    # Parent attribute
    attribute: Attribute = None

    def __post_init__(self):
        """
        """
        self.value = None

    def set_attribute(self, attribute):
        """Attach the field to its parent attribute
        """
        self.attribute = attribute

# -----------------------------------------------------------------------------

@dataclass
class RoField(Field):
    """Read Only Field
    """
    
    def supported(self):
        """Return True if this field is supported by the attribute
        """
        return self.attribute.support(self.name)
    
    def get(self):
        """Attribute is the one holding the data
        """
        return self.attribute.get(self.name)

# -----------------------------------------------------------------------------

@dataclass
class RwField(RoField):
    """Read Write Field
    """
    
    def set(self, val, ensure=True):
        """To write the field
        """
        self.attribute.set(**{self.name: val, "ensure": ensure})

