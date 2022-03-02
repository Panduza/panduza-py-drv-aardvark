# Imports
import threading
from aardvark_py import *
from loguru import logger


class AardvarkBridge:
    """Centralized aardvark connection manager
    """

    # {
    #   serial: {  handle:  ,   }
    # }
    CACHE = {}
    
    #
    MUTEX = threading.Lock()

    @staticmethod
    def GetHandle(serial_number):
        """Find the aardvark device with the given serial number
        """
        
        AardvarkBridge.MUTEX.acquire()
        
        #
        sn_str = str(serial_number)
        if sn_str in AardvarkBridge.CACHE:
            return AardvarkBridge.CACHE[sn_str]["handle"]

        # Start by running an extended discovery
        MAX_NUMBER_OF_DEVICE_TO_DETECT=32
        aa_devices_extended = aa_find_devices_ext(MAX_NUMBER_OF_DEVICE_TO_DETECT, MAX_NUMBER_OF_DEVICE_TO_DETECT)

        # Get the number of connected aardvark
        number_of_connected_aardvark = aa_devices_extended[0]
        if number_of_connected_aardvark == 0:
            raise Exception("No aardvark connected")

        # Get the index of the port of the aardvark we want to control
        index_of_the_port=0
        try:
            index_of_the_port = aa_devices_extended[2].index(serial_number)
        except ValueError:
            raise Exception(f"Aadvark with serial id {serial_number} not connected")

        # Take the port of the first device found
        port_aardvark = aa_devices_extended[1][index_of_the_port]

        # Open the device port
        aardvark_handle = aa_open(port_aardvark)
        logger.debug(f"open aardvark {serial_number} on port {port_aardvark}")
        if aardvark_handle < 0:
            raise Exception(f"Error opening aardvark '{aa_status_string(aardvark_handle)}'")

        #
        AardvarkBridge.CACHE[sn_str] = { "handle": aardvark_handle }

        AardvarkBridge.MUTEX.release()
        
        # Return the handle
        return aardvark_handle

    @staticmethod
    def ConfigureSpiMaster(handle, bitrate_khz, cpol, cpha, bitorder, ss_polarity):
        """Configure the aardvark as spi master

        Args:
            handle (_type_): handle of the aardvark
            bitrate_khz (_type_): _description_
            cpol (_type_): _description_
            cpha (_type_): _description_
            bitorder (_type_): _description_
            ss_polarity (_type_): _description_
        """
        aa_spi_bitrate(handle, bitrate_khz)
        aa_spi_configure(handle, cpol, cpha, bitorder)
        aa_spi_slave_disable(handle)
        aa_spi_master_ss_polarity(handle, ss_polarity)


    @staticmethod
    def ConfigureSpiSlave(handle, bitrate_khz, cpol, cpha, bitorder):
        """Configure the aardvark as spi slave

        Args:
            handle (_type_): handle of the aardvark
            bitrate_khz (_type_): _description_
            cpol (_type_): _description_
            cpha (_type_): _description_
            bitorder (_type_): _description_
            ss_polarity (_type_): _description_
        """
        aa_spi_bitrate(handle, bitrate_khz)
        aa_spi_configure(handle, cpol, cpha, bitorder)
        aa_spi_slave_enable(handle)


    @staticmethod
    def ConfigureTwiMaster(handle, bitrate_khz):
        #
        aa_i2c_bitrate(handle, bitrate_khz)


    @staticmethod
    def ConfigureTwiSlave(handle, bitrate_khz, slave_addr):
        aa_i2c_bitrate(handle, bitrate_khz)
        aa_i2c_slave_enable(handle, slave_addr, 1024, 1024)


