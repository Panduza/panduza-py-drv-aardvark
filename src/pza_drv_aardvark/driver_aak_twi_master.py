import time
import base64
from loguru import logger
from pza_platform import MetaDriver
from .bridge import AardvarkBridge
from aardvark_py import *

class DriverAardvarkTwiMaster(MetaDriver):
    """ Driver Aardvark twi Master
    """

    ###########################################################################
    ###########################################################################
    
    def config(self):
        """ FROM MetaDriver
        """
        return {
            "compatible": "aardvark_twi_master",
            "info": { "type": "twi/master", "version": "1.0" },
            "settings": {
                "serial_number": "serial number of the aardvark you want to use for this interface as an integer (2237170206)",
            }
        }
        # "bitrate_hz": "spi bitrate as an integer in hz (4000000)",
        # "clock_polarity": "CPOL [0 / 1]",
        # "clock_phase": "CPHA [0 / 1]",
        # "bitorder": "[msb / lsb] first",
        # "ss_polarity": "[active_low / active_high]"

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

        #
        logger.debug(f"bitrate: {self.bitrate_khz}khz")

        #
        AardvarkBridge.ConfigureTwiMaster(self.aa_handle, self.bitrate_khz)


        # Register commands
        self.register_command("data/read", self.__data_read)
        self.register_command("data/write", self.__data_write)

        
    ###########################################################################
    ###########################################################################

    def loop(self):
        """ FROM MetaDriver
        """
        return False

    ###########################################################################
    ###########################################################################

    def __data_write(self, payload):
        """
        """
        # Debug log
        logger.debug(f"CMD data/write ({payload})")

        # Parse the params
        req = self.payload_to_dict(payload)
        data = base64.b64decode(req["data"])
        addr = req["addr"]
        
        flags = AA_I2C_NO_FLAGS
        if "addr_10b" in req and req["addr_10b"]:
            flags = flags | AA_I2C_10_BIT_ADDR
        if "no_stop" in req and req["no_stop"]:
            flags = flags | AA_I2C_NO_STOP

        #
        status = aa_i2c_write(self.aa_handle, addr, flags, array('B', data) )
        if status < 0:
            print(f"fail sending data ({aa_status_string(status)})")
            return
    
        logger.debug(f"CMD data/read ({payload})")


    ###########################################################################
    ###########################################################################

    def __data_read(self, payload):
        """
        """
        # Debug log
        logger.debug(f"CMD data/read ({payload})")


