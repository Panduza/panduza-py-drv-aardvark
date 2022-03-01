import time
import json
import base64
from loguru import logger
from pza_platform import MetaDriver
from .bridge import AardvarkBridge
from aardvark_py import *

class DriverAardvarkSpiMaster(MetaDriver):
    """ Driver Aardvark Spi Master
    """

    ###########################################################################
    ###########################################################################
    
    def config(self):
        """ FROM MetaDriver
        """
        return {
            "compatible": "aardvark_spi_master",
            "info": { "type": "spi/master", "version": "1.0" },
            "settings": {
                "serial_number": "serial number of the aardvark you want to use for this interface as an integer (2237170206)",
                "bitrate_hz": "spi bitrate as an integer in hz (4000000)",
                "clock_polarity": "CPOL [0 / 1]",
                "clock_phase": "CPHA [0 / 1]",
                "bitorder": "[msb / lsb] first",
                "ss_polarity": "[active_low / active_high]"
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

        # Slave Select Polarity
        self.ss_polarity = AA_SPI_SS_ACTIVE_LOW
        if "ss_polarity" in tree["settings"]:
            if tree["settings"]["ss_polarity"] == "active_low":
                self.ss_polarity = AA_SPI_SS_ACTIVE_LOW
            else:
                self.ss_polarity = AA_SPI_SS_ACTIVE_HIGH

        #
        logger.debug(f"bitrate: {self.bitrate_khz}khz")
        logger.debug(f"CPOL: {self.cpol}")
        logger.debug(f"CPHA: {self.cpha}")
        logger.debug(f"bitorder: {tree['settings']['bitorder']} / {self.bitorder}")
        logger.debug(f"ss-polarity: {tree['settings']['ss_polarity']} / {self.ss_polarity}")
        
        #
        AardvarkBridge.ConfigureSpiMaster(self.aa_handle, self.bitrate_khz, self.cpol, self.cpha, self.bitorder, self.ss_polarity)
        
        # Register commands
        self.register_command("data/transfer", self.__data_transfer)

    ###########################################################################
    ###########################################################################

    def loop(self):
        """ FROM MetaDriver
        """
        return False

    ###########################################################################
    ###########################################################################

    def __data_transfer(self, payload):
        """
        """

        # log
        logger.debug(f"Data transfer requested {payload}")
        
        # Parse the params
        req = self.payload_to_dict(payload)
        data_to_send = base64.b64decode(req["data"])
        
        write_only = req["write_only"]

        #
        status, data_in = aa_spi_write(self.aa_handle, array('B', data_to_send), 999999)
        if status < 0:
            print(f"fail sending data ({aa_status_string(status)})")


        if not write_only:
            payload_dict = {
                "data": base64.b64encode(data_in).decode('ascii')
            }
            self.push_attribute("data", json.dumps(payload_dict))


        # print("MASTER input", data_in, "\n")


