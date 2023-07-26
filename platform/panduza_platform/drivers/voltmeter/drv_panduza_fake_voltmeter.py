import asyncio
from meta_drivers.voltmeter import MetaDriverVoltmeter


class DriverFakeVoltmeter(MetaDriverVoltmeter):
    """Fake Voltmeter driver
    """

    # =============================================================================
    # FROM MetaDriverVoltmeter

    def _PZA_DRV_VOLTMETER_config(self):
        """
        """
        return {
            "name": "panduza.fake.voltmeter",
            "description": "Virtual VOLTMETER"
        }

    # ---

    async def _PZA_DRV_loop_init(self, loop, tree):
        """Init function
        Reset fake parameters
        """

        settings = tree.get("settings", {})
        # self.log.info(settings)

        # work_with_fake_bps = settings.get("work_with_fake_bps", None)
        # self.bps_obj = self.get_interface_instance_from_pointer(work_with_fake_bps)

        
        self.__task_increment = loop.create_task(self.__increment_task())


        self.__fakes = {
            "measure": {
                "value": 0
            }
        }

        # Call meta class BPS ini
        await super()._PZA_DRV_loop_init(loop, tree)

    # ---

    async def _PZA_DRV_VOLTMETER_read_measure_value(self):
        return self.__fakes["measure"]["value"]

    # ---

    async def __increment_task(self):
        while True:
            await asyncio.sleep(0.2)
            self.__fakes["measure"]["value"] += 0.001
