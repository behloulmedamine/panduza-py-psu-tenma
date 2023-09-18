import asyncio

from hamcrest import assert_that, has_key, instance_of
from meta_drivers.servomotor import MetaDriverServomotor
from connectors.uart_ftdi_serial import ConnectorUartFtdiSerial


class DriverServomotor(MetaDriverServomotor):
    """Fake Voltmeter driver
    """

    # =============================================================================
    # FROM MetaDriverVoltmeter

    def _PZA_DRV_SERVOMOTOR_config(self):
        """
        """
        return {
            "name": "panduza.servomotor",
            "description": "Virtual SERVOMOTOR"
        }

    # ---

    async def _PZA_DRV_loop_init(self, loop, tree):
        """Init function
        Reset fake parameters
        """

        settings = tree.get("settings", {})
        # self.log.info(settings)

         # Checks
        assert_that(settings, has_key("serial_port_name"))
        assert_that(settings, has_key("serial_baudrate"))
        assert_that(settings, has_key("number_of_servo"))
        

        self.number_of_servo = settings["number_of_servo"]
        
        #self.__task_increment = loop.create_task(self.__increment_task())

        # Get the gate connector
        self.uart_connector = await ConnectorUartFtdiSerial.Get(loop,**settings)


        self.__fakes = {
            "position": {
                "value": 0
            }
        }

        # Call meta class BPC ini
        await super()._PZA_DRV_loop_init(loop, tree)

    # ---

    async def _PZA_DRV_SERVOMOTOR_get_position_value(self):
        
        await self.uart_connector.write_uart(f"get")
        
        self.__fakes["position"]["value"] = await self.uart_connector.read_uart()
        print(self.__fakes["position"]["value"])
        
        return self.__fakes["position"]["value"]
    
        # tab = []

        #first_response = await self.uart_connector.read_uart()

        # if first_response == "start": 
        #     for i in range(self.number_of_servo):
        #         response = await self.uart_connector.read_uart()
        #         self.__fakes["position"]["value"] = response
        #         print(response)
                
        #     #self.__fakes["position"]["value"] = tab[i]
        #     #print (tab)
        
        #     return self.__fakes["position"]["value"]

    

        
    
    
    
    async def _PZA_DRV_SERVOMOTOR_set_position_value(self,id,value):
        await self.uart_connector.write_uart(f"set {id} {value}")
        self.__fakes["position"]["value"] = value
    
        return self.__fakes["position"]["value"]

    # ---

    # async def __increment_task(self):
    #     while True:
    #         await asyncio.sleep(0.2)
    #         self.__fakes["position"]["value"] += 0.001
