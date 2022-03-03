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

        # Get bitrate
        self.bitrate_khz = 1000
        if "bitrate_hz" in tree["settings"]:
            self.bitrate_khz = int(tree["settings"]["bitrate_hz"] / 1000)

        #
        self.address = 42
        if "address" in tree["settings"]:
            self.address = tree["settings"]["address"]
 
        #
        logger.debug(f"bitrate: {self.bitrate_khz}khz")
        logger.debug(f"address: {self.address}")

        #
        AardvarkBridge.ConfigureTwiSlave(self.aa_handle, self.bitrate_khz, self.address)

    ###########################################################################
    ###########################################################################

    def loop(self):
        """ FROM MetaDriver
        """
        # Poll on events and trigger if spi event
        event = aa_async_poll(self.aa_handle, 0)
        
        if event & AA_ASYNC_I2C_READ:
            print("- event I2C read")
            status, addr, data_in = aa_i2c_slave_read(self.aa_handle, 99999)
            if status < 0:
                print(aa_status_string(status))
            print(f"from addr {addr} data recieved {data_in}")


        if event & AA_ASYNC_I2C_WRITE:
            print("- event I2C write")

            # Get number of bytes written to master
            num_bytes = aa_i2c_slave_write_stats(self.aa_handle)

            if (num_bytes < 0):
                print("error: %s" % aa_status_string(num_bytes))

            # Print status information to the screen
            print(f"Number of bytes written to master: {num_bytes}")

            # return True

        return False


