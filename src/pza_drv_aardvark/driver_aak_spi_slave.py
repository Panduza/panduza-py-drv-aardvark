import time
from loguru import logger
from .bridge import AardvarkBridge
from pza_platform import MetaDriverIo
from aardvark_py import *

class DriverAardvarkSpiSlave(MetaDriverIo):
    """ Driver Aardvark Spi Slave
    """

    ###########################################################################
    ###########################################################################

    def config(self):
        """ FROM MetaDriver
        """
        return {
            "compatible": "aardvark_spi_slave",
            "info": { "type": "spi/slave", "version": "1.0" },
            "settings": {
                "serial_number": "serial number of the aardvark you want to use for this interface as an integer (2237170206)",
                "bitrate_hz": "spi bitrate as an integer in hz (4000000)",
                "clock_polarity": "CPOL [0 / 1]",
                "clock_phase": "CPHA [0 / 1]",
                "bitorder": "[msb / lsb] first"
            }
        }

    ###########################################################################
    ###########################################################################

    def setup(self, tree):
        """ FROM MetaDriver
        """
        # Open the device
        self.aa_handle = AardvarkBridge.GetHandle( tree["settings"]["serial_number"] )
        
        # Get bitrate
        self.bitrate_khz = 1000
        if "bitrate_hz" in tree["settings"]:
            self.bitrate_khz = int(tree["settings"]["bitrate_hz"] / 1000)

        # Get Polarities
        self.cpol = 0
        self.cpha = 0
        if "clock_polarity" in tree["settings"]:
            self.cpol = tree["settings"]["clock_polarity"]
        if "clock_phase" in tree["settings"]:
            self.cpha = tree["settings"]["clock_phase"]

        # Get Bitorder
        self.bitorder = AA_SPI_BITORDER_MSB
        if "bitorder" in tree["settings"]:
            if tree["settings"]["bitorder"] == "msb":
                self.bitorder = AA_SPI_BITORDER_MSB
            else:
                self.bitorder = AA_SPI_BITORDER_LSB

        #
        logger.debug(f"bitrate: {self.bitrate_khz}khz")
        logger.debug(f"CPOL: {self.cpol}")
        logger.debug(f"CPHA: {self.cpha}")
        logger.debug(f"bitorder: {tree['settings']['bitorder']} / {self.bitorder}")
        logger.debug(f"ss-polarity: active_low forced on aardvark slaves")
        
        #
        AardvarkBridge.ConfigureSpiSlave(self.aa_handle, self.bitrate_khz, self.cpol, self.cpha, self.bitorder)
        

    ###########################################################################
    ###########################################################################
        
    def loop(self):
        """ FROM MetaDriver
        """

        event = aa_async_poll(self.aa_handle, 0)
        if event & AA_ASYNC_SPI:

            data_in=array('B', [0,0,0,0,0,0,0,0])
            status, data_in = aa_spi_slave_read(self.aa_handle, data_in)
            if status < 0:
                print(aa_status_string(status))
            print(data_in)
            return True

        # logger.debug(f"event {event}")

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



