#!/usr/bin/env python

"""
This is the updater script for the ION 7350 interface to BuildingOS. Every X hours, where
X is some number between 2 and 12 (larger intervals are not good), downloads reading data
from the past X hours for each meter listed in an input csv file, packages it into a JSON
object as per Lucid's Connector API, and pushes that object to BuildingOS.
"""

import os
import sys
import LbnlIon7350Interface.getter
import LbnlIon7350Interface.processor
import LbnlIon7350Interface.loader

from LbnlIon7350Interface.utils import utils
from LbnlIon7350Interface.utils import read_creds
from LbnlIon7350Interface.utils import Cursor
from LbnlIon7350Interface.utils import defaults


def _usage():
    string = "USAGE:\n\tpython interface.py [interval]\n"
    print(string)

def main():
    if len(sys.argv) < 2:
        utils.error('Requires an integer interval argument')
        _usage()
        exit()
    try:
        interval = int(sys.argv[1])
    except ValueError:
        utils.error('Requires an integer interval argument')
        exit()
    getter.run_update()

if __name__ == '__main__':
    main()
