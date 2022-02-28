from behave import *
from panduza import SpiMaster

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

    context.spi = {}
    context.spi[spi_master] = SpiMaster(alias=spi_master)
    context.spi[spi_master].enableWatchdog()
    assert context.spi[spi_master].isAlive() is True

    context.spi[spi_master].disableWatchdog()

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
    pass


