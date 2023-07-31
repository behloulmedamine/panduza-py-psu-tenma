import abc
import json
import time
import inspect
from collections import ChainMap
from core.platform_driver import PlatformDriver

class MetaDriverDio(PlatformDriver):

    # =============================================================================
    # PLATFORM DRIVERS FUNCTIONS

    def _PZA_DRV_config(self):
        """Driver base configuration
        """
        base = {
            "info": {
                "type": "dio",
                "version": "0.0"
            }
        }
        return ChainMap(base, self._PZA_DRV_DIO_config())

    # ---

    async def _PZA_DRV_loop_init(self, loop, tree):
        """From PlatformDriver
        """
        # Set handers
        self.__cmd_handlers = {
            "direction" : self.__handle_cmds_set_direction,
            "state" : self.__handle_cmds_set_state,
        }

        # first update
        await self.__update_attribute_initial()

        # Init Success
        await super()._PZA_DRV_loop_init(loop, tree)

    # ---

    # def _PZA_DRV_loop_run(self, loop):
    #     # polls
    #     # self.__poll_att_direction()
    #     # self.__poll_att_state()
    #     # time.sleep(0.1)
    #     pass

    # ---

    # =============================================================================
    # TO OVERRIDE IN DRIVER

    # ---

    def _PZA_DRV_DIO_config(self):
        """Driver base configuration
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    async def _PZA_DRV_DIO_get_direction_value(self):
        """ get value of direction value
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    async def _PZA_DRV_DIO_set_direction_value(self, value):
        """ set value of direction value

        -  Args
            value : value to be set : in or out
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    async def _PZA_DRV_DIO_get_direction_pull(self):
        """ get direction pull
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    async def _PZA_DRV_DIO_set_direction_pull(self, v):
        """ set the pull direction
        -Args
        value : value to be set : up, down or open
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    async def _PZA_DRV_DIO_get_state_active(self):
        """ get the active state
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    async def _PZA_DRV_DIO_set_state_active(self,v):
        """ get the active state
        -Args
        value : value to be set : True or False
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    async def _PZA_DRV_DIO_get_state_activeLow(self):
        """ get the active low state
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    async def _PZA_DRV_DIO_set_state_activeLow(self,v):
        """ set the active low state
            -Args
            value : value to be set : True or False
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # =============================================================================
    # PRIVATE FUNCTIONS

    # ---

    async def __update_attribute_initial(self):
        """Function to perform the initial init
        """
        await self.__att_direction_full_update()
        await self.__att_state_full_update()


    # ---

    async def __handle_cmds_set_direction(self, cmd_att):
        """
        """
        update_obj = {}
        await self._prepare_update(update_obj, 
                            "direction", cmd_att,
                            "value", [str]
                            , self._PZA_DRV_DIO_set_direction_value
                            , self._PZA_DRV_DIO_get_direction_value)
        await self._prepare_update(update_obj, 
                            "direction", cmd_att,
                            "pull", [str]
                            , self._PZA_DRV_DIO_set_direction_pull
                            , self._PZA_DRV_DIO_get_direction_pull)
        await self._update_attributes_from_dict(update_obj)

    # ---

    async def __handle_cmds_set_state(self, cmd_att):
        """
        """
        update_obj = {}
        await self._prepare_update(update_obj, 
                            "state", cmd_att,
                            "active", [bool]
                            , self._PZA_DRV_DIO_set_state_active
                            , self._PZA_DRV_DIO_get_state_active)
        await self._prepare_update(update_obj, 
                            "state", cmd_att,
                            "active_low", [bool]
                            , self._PZA_DRV_DIO_set_state_activeLow
                            , self._PZA_DRV_DIO_get_state_activeLow)
        await self._update_attributes_from_dict(update_obj)

    # ---

    async def __att_direction_full_update(self):
        """Just update all field of direction
        """
        await self._update_attributes_from_dict({
            "direction": {
                "value": await self._PZA_DRV_DIO_get_direction_value(),
                "pull": await self._PZA_DRV_DIO_get_direction_pull(),
                "polling_cycle": 1
            }
        })

    # ---

    async def __att_state_full_update(self):
        """Just update all field of direction
        """
        await self._update_attributes_from_dict({
            "state": {
                "active": await self._PZA_DRV_DIO_get_state_active(),
                "active_low": await self._PZA_DRV_DIO_get_state_activeLow(),
                "polling_cycle": 1
            }
        })


    # def __poll_att_direction(self):

    #     polling_cycle = float(self._get_field("direction", "polling_cycle"))
        
    #     if polling_cycle < 0:
    #         return
    #     if (time.perf_counter() - self.polling_ref["direction"]) > polling_cycle:
    #         p = False
    #         p = await self._update_attribute("direction", "pull", self._PZA_DRV_DIO_get_direction_pull(), False) or p
    #         p = await self._update_attribute("direction", "value", self._PZA_DRV_DIO_get_direction_value(), False) or p
    #         if p:
    #             self._push_attribute("direction")
    #         self.polling_ref["direction"] = time.perf_counter()


    # def __poll_att_state(self):
        
    #     polling_cycle = float(self._get_field("state", "polling_cycle"))
    #     value = bool(self._get_field("state", "active"))
    #     if polling_cycle < 0:
    #         return
    #     if (time.perf_counter() - self.polling_ref["state"]) > polling_cycle:
    #         p = False
    #         p = await self._update_attribute("state", "active", self._PZA_DRV_DIO_get_state_active(), False) or p
    #         p = await self._update_attribute("state", "active_low", self._PZA_DRV_DIO_get_state_activeLow(), False) or p
    #         if p:
    #             self._push_attribute("state")
    #         self.polling_ref["state"] = time.perf_counter()




