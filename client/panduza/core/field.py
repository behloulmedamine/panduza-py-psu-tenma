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
    
    def get(self):
        """
        """
        # self.attribute.set(**{self.name: val})
        pass


# -----------------------------------------------------------------------------

@dataclass
class RwField(RoField):
    """Read Write Field
    """
    
    def set(self, val, ensure=False):
        """To write the field
        """
        self.attribute.set(**{self.name: val, "ensure": ensure})

