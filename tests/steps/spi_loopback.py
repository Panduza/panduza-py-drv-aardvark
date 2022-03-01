from behave import *
from panduza import SpiMaster, SpiSlave

import time

###############################################################################
###############################################################################

# Required to parse arguments in steps, for example "{thing}"
use_step_matcher("parse")

###############################################################################
###############################################################################

@given('two spi interfaces "{spi_master}" and "{spi_slave}"')
def given_two_interfaces(context, spi_master, spi_slave):
    """
    """
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

@when('data "{data}" is emitted on spi "{spi_master}"')
def data_is_emitted_from_master(context, data, spi_master):
    """
    """
    context.spi[spi_master].transfer(bytearray(data.encode()), 0)
    
###############################################################################
###############################################################################

@then('data "{data}" must be received on spi "{spi_slave}"')
def data_must_be_received_on_slave(context, data, spi_slave):
    """
    """
    # On slave wait for incomming  data
    spi_s = context.spi[spi_slave]
    while not spi_s.has_pending_data():
        pass

    # Pop the data
    received_data = spi_s.pop_data()

    # Decode and test
    assert received_data.decode() == data

###############################################################################
###############################################################################

@when('data "{data}" is configured as response on spi "{spi_slave}"')
def data_is_configured_as_response_on_spi_slave(context, data, spi_slave):
    """
    """
    spi_s = context.spi[spi_slave]
    spi_s.push_response(bytearray(data.encode()))

###############################################################################
###############################################################################

@then('data "{data}" must be received by spi "{spi_master}" when it requests a transfer')
def data_must_be_received_by_spi_when_requested_byt_master(context, data, spi_master):
    """_summary_
    """
    spi_m = context.spi[spi_master]
    spi_m.transfer(bytearray(len(data)), len(data))


    time.sleep(1)


