from behave import *
from panduza import SpiMaster, SpiSlave

import time

###############################################################################
###############################################################################

# Required to parse arguments in steps, for example "{thing}"
use_step_matcher("parse")

###############################################################################
###############################################################################

@given('two interfaces "{spi_master}" and "{spi_slave}"')
def given_two_interfaces(context, spi_master, spi_slave):
    print(spi_master, spi_slave)

    # Context Spi
    context.spi = {}
    
    # 
    spi_m = SpiMaster(alias=spi_master)
    spi_m.enableWatchdog()
    assert spi_m.isAlive() == True
    spi_m.disableWatchdog()
    context.spi[spi_master] = spi_m
    
    # 
    spi_s = SpiSlave(alias=spi_slave)
    spi_s.enableWatchdog()
    assert spi_s.isAlive() == True
    spi_s.disableWatchdog()
    context.spi[spi_slave] = spi_s

###############################################################################
###############################################################################

@when('data "{data}" is emitted on "{spi_master}"')
def data_is_emitted(context, data, spi_master):
    # assert context.spi_master.isAlive() is True

    
    context.spi[spi_master].transfer(bytearray(data.encode()), 0)
    

###############################################################################
###############################################################################

@then('data "{data}" must be received on "{spi_slave}"')
def data_is_emitted(context, data, spi_slave):
    time.sleep(1)
    
    # context.spi[spi_slave] 
    

