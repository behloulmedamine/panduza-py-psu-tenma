import time
import logging
from dataclasses import dataclass, field

from .field import RoField, RwField
from .attribute import Attribute
from .helper import payload_to_dict


@dataclass
class AttributeInfo(Attribute):

    name: str = "info"
    retain: bool = False

    def __post_init__(self):
        super().__post_init__()
        self.info = {}
        self.last_update_time = None

    def _on_att_message(self, topic, payload):
        self.info = payload_to_dict(payload)['info']
        self.last_update_time = time.time()

    def ping(self):
        # TODO just ping the given interface
        self.interface.client.publish("pza", b"*")

    def get_type(self):
        return self.info.get("type", "unknown")

    def get_state(self):
        return self.info.get("state", "unknown")


