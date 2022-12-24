#!/usr/bin/env python3
"""
Polyglot v3 node server Lighting Version
Copyright (C) 2021 For James Paul Modified by Steven Bailey
"""
import logging
from nodes import tuya_light_node
from nodes import tuya_switch_node
from nodes import TuyaNode
from nodes import Tuya_Controller
import udi_interface
import sys

LOGGER = udi_interface.LOGGER
LOG_HANDLER = udi_interface.LOG_HANDLER


if __name__ == "__main__":
    try:
        LOGGER.debug("Staring Tuya Interface")
        polyglot = udi_interface.Interface([Tuya_Controller, TuyaNode])
        polyglot.start()
        control = Tuya_Controller(
            polyglot, 'controller', 'controller', 'Tuya Controller')
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        polyglot.stop()
        sys.exit(0)
    except Exception as err:
        LOGGER.error('Excption: {0}'.format(err), exc_info=True)
        sys.exit(0)
