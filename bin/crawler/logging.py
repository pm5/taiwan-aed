#!/usr/bin/env python

import logging
from os import getenv

default_logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
default_logger.addHandler(handler)

if getenv('DEBUG') != None:
    default_logger.setLevel(logging.DEBUG)
else:
    default_logger.setLevel(logging.INFO)
