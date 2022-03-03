import time
from behave import *
from panduza import TwiMaster, TwiSlave
from xdocz_helpers import AttachTextLog

###############################################################################
###############################################################################

# Required to parse arguments in steps, for example "{thing}"
use_step_matcher("parse")

###############################################################################
###############################################################################

@given('two twi interfaces "{twi_master}" and "{twi_slave}"')
def given_two_interfaces(context, twi_master, twi_slave):
    """
    """
    # Context twi
    context.twi = {}

    # Create interfaces
    twi_m = TwiMaster(alias=twi_master)
    twi_s = TwiSlave(alias=twi_slave)

    # Log
    AttachTextLog(context, f"Twi Slave  Topic ({twi_s.baseTopic})")
    AttachTextLog(context, f"Twi Master Topic ({twi_m.baseTopic})")

    # 
    twi_m.enableHeartBeatMonitoring()
    assert twi_m.isAlive() == True
    twi_m.disableHeartBeatMonitoring()
    context.twi[twi_master] = twi_m
    
    # 
    twi_s.enableHeartBeatMonitoring()
    assert twi_s.isAlive() == True
    twi_s.disableHeartBeatMonitoring()
    context.twi[twi_slave] = twi_s

###############################################################################
###############################################################################

@when('data "{data}" is written on twi master "{twi_master}"')
def when_data_is_emitted_on_twi_master(context, data, twi_master):
    """
    """
    # Local vars
    twi_m = context.twi[twi_master]
    # Write data
    twi_m.write(bytearray(data.encode()))


