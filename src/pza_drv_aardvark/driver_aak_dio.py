import time
from loguru import logger
from pza_platform import MetaDriverIo

class DriverAardvarkDio(MetaDriverIo):
    """
    """

    ###########################################################################
    ###########################################################################
    
    def config(self):
        """ FROM MetaDriver
        """
        return {
            "compatible": "aardvark_io",
            "info": { "type": "io/digital", "version": "1.0" }
        }

    ###########################################################################
    ###########################################################################

    def setup(self, tree):
        """ FROM MetaDriver
        """
        # # Initialize variables
        # self._loop=0
        # self.id = tree["gpio"]["id"]
        # self.value = -1
        # self.direction = None

        # # Try to export the gpio
        # self.__export()

        # # Register commands
        # self.register_command("value/set", self.__set_value)
        # self.register_command("direction/set", self.__set_direction)

    ###########################################################################
    ###########################################################################
        
    def loop(self):
        """ FROM MetaDriver
        """
        # if self._loop % 2 == 0:
        #     self.__push_attribute_value()
        #     self.__push_attribute_direction()
        # self._loop += 1
        # time.sleep(0.5)
        return False

    # ###########################################################################
    # ###########################################################################

    # def __export(self):
    #     """ Export the gpio
    #     """
    #     try:
    #         f = open("/sys/class/gpio/export", "w")
    #         f.write(str(self.id))
    #         f.close()
    #         logger.info("export gpio id:{}", self.id)
    #     except IOError as e:
    #         if e.errno == 16:
    #             logger.debug("gpio {} already exported", self.id)
    #         else:
    #             raise Exception("Error exporting GPIOs %s | %s" % (str(self.id), repr(e)))

    # ###########################################################################
    # ###########################################################################

    # def __set_value(self, payload):
    #     """
    #     """
    #     # Parse request
    #     req = self.payload_to_dict(payload)
    #     req_value = req["value"]
    #     self.value=req_value

    #     try:
    #         path = "/sys/class/gpio/gpio%s/value" % self.id
    #         f = open(path, "w")         
    #         # Update value
    #         f.write(str(self.value))
    #         self.push_io_value(self.value)
    #         # log
    #         logger.info(f"new value : {self.value}")

    #         f.close()
    #     except IOError as e:
    #         # mogger.error("Unable to set value %s to GPIO %s (%s) | %s", str(val), self.id, path, repr(e))
    #         pass

    # ###########################################################################
    # ###########################################################################

    # def __set_direction(self, payload):
    #     """
    #     """
    #     # Parse request
    #     req = self.payload_to_dict(payload)
    #     req_direction = req["direction"]
    #     # Update direction
    #     self.direction=req_direction
    #     # log
    #     logger.info(f"new direction : {self.direction}")

    #     try:
    #         f = open("/sys/class/gpio/gpio%s/direction" % self.id, "w")
    #         f.write(self.direction)
    #         self.push_io_direction(self.direction)
    #         f.close()
    #     except IOError:
    #         # mogger.error("Unable to export set value")
    #         pass

    # ###########################################################################
    # ###########################################################################

    # def __push_attribute_value(self):
    #     """ To read and push value attribute of the gpio
    #     """
    #     if self.direction == 'out':
    #         return

    #     try:
    #         # Read the value from the driver
    #         f = open("/sys/class/gpio/gpio%s/value" % self.id, "r")
    #         value = f.read(1)
    #         f.close()
    #         value = int(value)

    #         # Push the attribute if it changed
    #         if self.value != value:
    #             self.value = value
    #             logger.debug("gpio '{}' value modified : {}", self.name, self.value)
    #             self.push_io_value(self.value)
    #     except IOError as e:
    #         logger.error("Unable to get value %s", repr(e))

    # ###########################################################################
    # ###########################################################################

    # def __push_attribute_direction(self):
    #     """ To read and push direction attribute of the gpio
    #     """
    #     try:
    #         # Read the direction from the driver
    #         f = open("/sys/class/gpio/gpio%s/direction" % self.id, "r")
    #         direction = f.read()
    #         f.close()
    #         direction = direction.rstrip("\n")

    #         # Push the attribute if it changed
    #         if self.direction != direction:
    #             self.direction = direction
    #             logger.debug("gpio '{}' direction modified : {}", self.name, self.direction)
    #             self.push_io_direction(self.direction)
    #     except IOError:
    #         logger.error("Unable to get direction %s", repr(e))



