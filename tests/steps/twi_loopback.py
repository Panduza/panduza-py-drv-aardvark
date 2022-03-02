from behave import *
from panduza import TwiMaster, TwiSlave

import time

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
    
    # 
    twi_m = TwiMaster(alias=twi_master)
    twi_m.enableHeartBeatMonitoring()
    assert twi_m.isAlive() == True
    twi_m.disableHeartBeatMonitoring()
    context.twi[twi_master] = twi_m
    
    # 
    twi_s = TwiSlave(alias=twi_slave)
    twi_s.enableHeartBeatMonitoring()
    assert twi_s.isAlive() == True
    twi_s.disableHeartBeatMonitoring()
    context.twi[twi_slave] = twi_s

