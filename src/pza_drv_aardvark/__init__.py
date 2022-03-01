from .driver_aak_io_digital import DriverAardvarkIoDigital
from .driver_aak_spi_slave import DriverAardvarkSpiSlave
from .driver_aak_spi_master import DriverAardvarkSpiMaster
from .driver_aak_twi_slave import DriverAardvarkTwiSlave
from .driver_aak_twi_master import DriverAardvarkTwiMaster


PZA_DRIVERS_LIST=[
    DriverAardvarkIoDigital,
    DriverAardvarkSpiSlave,
    DriverAardvarkSpiMaster,
    DriverAardvarkTwiSlave,
    DriverAardvarkTwiMaster
]

