import time
import base64
from loguru import logger
from pza_platform import MetaDriver
from .bridge import AardvarkBridge
from aardvark_py import *

class DriverAardvarkTwiSlave(MetaDriver):
    """ Driver Aardvark twi Slave
    """

    ###########################################################################
    ###########################################################################
    
    def config(self):
        """ FROM MetaDriver
        """
        return {
            "compatible": "aardvark_twi_slave",
            "info": { "type": "twi/slave", "version": "1.0" },
            "description": "Mount a twi slave interface using an aardvark adapter",
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
        

    ###########################################################################
    ###########################################################################

    def loop(self):
        """ FROM MetaDriver
        """
        return False

