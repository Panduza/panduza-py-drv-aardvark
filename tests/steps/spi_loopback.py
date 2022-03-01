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
    spi_m.enableHeartBeatMonitoring()
    assert spi_m.isAlive() == True
    spi_m.disableHeartBeatMonitoring()
    context.spi[spi_master] = spi_m
    
    # 
    spi_s = SpiSlave(alias=spi_slave)
    spi_s.enableHeartBeatMonitoring()
    assert spi_s.isAlive() == True
    spi_s.disableHeartBeatMonitoring()
    context.spi[spi_slave] = spi_s
    

###############################################################################
###############################################################################

@when('data "{data}" is emitted on spi "{spi_master}"')
def data_is_emitted_from_master(context, data, spi_master):
    """
    """
    # Local vars
    spi_m = context.spi[spi_master]
    spi_m.transfer(bytearray(data.encode()), write_only=True)

###############################################################################
###############################################################################

@then('data "{data}" must be received on spi "{spi_slave}"')
def data_must_be_received_on_slave(context, data, spi_slave):
    """
    """
    # Local vars
    spi_s = context.spi[spi_slave]

    # Slave wait for incomming data
    t0 = time.time()
    while (time.time() - t0 < 3) and not spi_s.has_pending_data():
        pass
    assert (time.time() - t0 < 3), "timeout!"

    # Pop the data
    received_data = spi_s.pop_data()
    context.attach("text/plain", f"data received by spi slave is {received_data}")

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
def data_must_be_received_by_spi_when_requested_by_master(context, data, spi_master):
    """_summary_
    """
    # Local vars
    spi_m = context.spi[spi_master]
 
    spi_m.transfer(bytearray(len(data)))

    # Slave wait for incomming data
    t0 = time.time()
    while (time.time() - t0 < 3) and not spi_m.has_pending_data():
        pass
    assert (time.time() - t0 < 3), "timeout!"

    # Pop the data
    received_data = spi_m.pop_data()
    context.attach("text/plain", f"data received by spi master is {received_data}")

    # Decode and test
    assert received_data.decode() == data



