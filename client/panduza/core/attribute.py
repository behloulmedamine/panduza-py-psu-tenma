import os
import json
import logging
import threading

from abc import ABC, abstractmethod
from typing      import Optional, Callable, Set
from dataclasses import dataclass, field

from .client import Client

from .helper import topic_join

# -----------------------------------------------------------------------------

class EnsureError(Exception):
    """ @brief Error raised when ensure tiemout is reached
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[ERROR] %s\n" % str(self.message)

# -----------------------------------------------------------------------------

@dataclass
class Attribute:
    name: str
    interface = None

    
    def __post_init__(self):
        """Initialize topics and logging
        """
        self._log = logging.getLogger(f"att={self.name}")
        self._field_data = {}


    def set_interface(self, interface):
        self.interface = interface
        self._topic_atts = topic_join(self.interface.topic, "atts", self.name)
        self._topic_cmds_set = topic_join(self.interface.topic, "cmds", "set")

        # Subscribe to topic
        self._log.debug(f"topic atts : {self._topic_atts}")
        self.interface.client.subscribe(self._topic_atts, callback=self._on_att_message)

        # print("sub \n", self._topic_atts)

    def _on_att_message(self, topic, payload):
        self._log.info(f"Received new value {payload}")
        # print("Received new value\n")

    #     if payload is None:
    #         self.__value = None
    #     else:
    #         self.__value = self.payload_parser(payload)
    #         self.__trigger.set()
    

    def add_field(self, field):
        """Append a field to the attribute
        """
        field.set_attribute(self)
        setattr(self, field.name, field)
        return self

    # ---

    @abstractmethod
    def get(self):
        pass

    # ---

    def set(self, **kwargs):
        """Send a set command
        """
        # Get ensure flag
        ensure=kwargs.get('ensure', False)

        # Prepare the payload
        kwargs.pop('ensure', None)
        pyl={}
        for key, value in kwargs.items():
            # TODO Check if the key match a field name
            pyl[key] = value
        cmd={}
        cmd[self.name] = pyl

        # Send message
        self.interface.client.publish_json(self._topic_cmds_set, cmd)

        # If ensure flag is set, wait for it
        if ensure:
            while True:
                pass

###############################################################################
###############################################################################

@dataclass
class Attribute_JSON(Attribute):
    __value: any = None

    def __post_init__(self):
        super().__post_init__()

        self.__trigger = threading.Event()

        # Subscribe to topic
        self.client.subscribe(self._topic_atts_get, callback=self.__update)


    def __del__(self):
        # Unsubscribe from topic
        self.client.unsubscribe(self._topic_atts_get, callback=self.__update)

    # ┌────────────────────────────────────────┐
    # │ Update callback                        │
    # └────────────────────────────────────────┘

    def __update(self, topic, payload):
        self._log.debug("Received new value")

        if payload is None:
            self.__value = None
        else:
            self.__value = self.payload_parser(payload)
            self.__trigger.set()
    

    # ┌────────────────────────────────────────┐
    # │ Trigger control                        │
    # └────────────────────────────────────────┘
    
    def trigger_arm(self):
        self.__trigger.clear()

    def trigger_wait(self, timeout):
        try:
            self.__trigger.wait(timeout=timeout)
        except:
            pass

    # ┌────────────────────────────────────────┐
    # │ Set/get                                │
    # └────────────────────────────────────────┘

    def get(self):
        return self.__value

    def set(self, v, ensure=False):
        """Set the attribute

        Args:
            v (_type_): The new value
            ensure (bool, optional): Set to true to wait for the confirmation that the command has been executed. Defaults to False.
        """

        retry=3
        if ensure:
            self.trigger_arm()

        self.client.publish(self._topic_cmds_set, self.payload_factory(v))

        if ensure:
            # It is possible that you catch some initialization message with the previous dir value
            # To manage this case, just wait for the correct value
            while self.__value != v and retry > 0:
                self.trigger_wait(timeout=1)
                if self.__value != v:
                    self.trigger_arm()
                    retry-=1

            if self.__value != v:
                raise RuntimeError(f"Attribute {self.name} for {self.base_topic}: cannot set to '{v}', got '{self.__value}'")


