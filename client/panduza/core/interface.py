import time
import json
import paho.mqtt.client as mqtt

from dataclasses import dataclass, field

from .core import Core
from .client import Client
from .helper import topic_join

from .attribute_info import AttributeInfo

@dataclass
class Interface:
    """Access point to a Panduza interface
    """

    alias : str = None
    addr : str = None
    port : int = None
    topic : str = None
    client : object = None
    ensure: bool = True

    def __post_init__(self):

        self._attribute_names = [] # authorized attribute names

        self.init(self.alias, self.addr, self.port, self.topic, self.client)

        # === INFO ===
        self.add_attribute(
            AttributeInfo()
        )

    # ---

    def init(self, alias=None, addr=None, port=None, topic=None, client=None):
        """Initialization of the interface

        **MUST BE KEPT FOR LATE INIT**
        """
        # Wait for later initialization
        if alias==None and addr==None and port==None and topic==None and client==None:
            return

        #
        if client != None:
            self.client = client
            self.topic = topic

        # Build a new client
        else:
            if alias:
                self.client = Client(interface_alias=alias)
                self.topic  = Core.BaseTopicFromAlias(alias)
            else:
                self.topic  = topic
                self.client = Client(url=addr, port=port)

        # 
        if not self.client.is_connected:
            self.client.connect()

    # ---

    def ensure_init(self):
        """Ensure that the interface has been initialized by the broker
        """
        for att in self._attribute_names:
            obj = getattr(self, att)
            obj.ensure_init()

    # ---

    def get_short_name(self):
        if self.alias:
            return self.alias
        else:
            return self.topic.split('/')[-1]

    # ---

    def add_attribute(self, attribute):
        # Append fields as attributes
        attribute.set_interface(self)
        setattr(self, attribute.name, attribute)
        self._attribute_names.append(attribute.name)
        return attribute

    # ---

    def payload_to_dict(self, payload):
        """ To parse json payload
        """
        return json.loads(payload.decode("utf-8"))

    # ---

    def payload_to_int(self, payload):
        """
        """
        return int(payload.decode("utf-8"))

    ###########################################################################
    ###########################################################################

    def payload_to_str(self, payload):
        """
        """
        return payload.decode("utf-8")

    # ###########################################################################
    # ###########################################################################

    # def isAlive(self):
    #     """
    #     """
    #     if not self.heart_beat_monitoring.enabled:
    #         raise Exception("watchdog not enabled on the interface")
        
    #     t0 = time.time()
    #     while (time.time() - t0 < 3) and not self.heart_beat_monitoring.alive:
    #         pass

    #     return self.heart_beat_monitoring.alive

    ###########################################################################
    ###########################################################################

    # def _on_info_message(self, client, userdata, msg):
    #     print("!!!", msg.topic)

        # if msg.topic.endswith('/info'):
        #     self.heart_beat_monitoring.update()

