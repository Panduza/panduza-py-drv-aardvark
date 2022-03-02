import time
import json
import base64
from loguru import logger
from .bridge import AardvarkBridge
from pza_platform import MetaDriver
from aardvark_py import *

class DriverAardvarkSpiSlave(MetaDriver):
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
        
        #
        self.register_command("responses/push", self.__responses_push)
        

    ###########################################################################
    ###########################################################################
        
    def loop(self):
        """ FROM MetaDriver
        """

        event = aa_async_poll(self.aa_handle, 0)
        if event & AA_ASYNC_SPI:

            status, data_in = aa_spi_slave_read(self.aa_handle, 99999)
            if status < 0:
                logger.warning(f"warning spi {aa_status_string(status)}")

            # Debug log
            logger.debug(f"data received: {data_in}")
            
            # Publish the data
            payload_dict = {
                "data": base64.b64encode(data_in).decode('ascii')
            }
            self.push_attribute("data", json.dumps(payload_dict))

 
            aa_spi_slave_set_response(self.aa_handle, array('B', bytearray()))


            return True

        # logger.debug(f"event {event}")

        return False

    ###########################################################################
    ###########################################################################

    def __responses_push(self, payload):
        """
        """
        # Parse request
        req = self.payload_to_dict(payload)
        data = base64.b64decode(req["data"])

        aa_spi_slave_set_response(self.aa_handle, array('B', data))



