#!/usr/bin/env python

"""
This is the updater script for the ION 7350 interface to BuildingOS. Every X hours, where
X is some number between 2 and 12 (larger intervals are not good), downloads reading data
from the past X hours for each meter listed in an input csv file, packages it into a JSON
object as per Lucid's Connector API, and pushes that object to BuildingOS.
"""

import os
import sys
from LbnlIon7350Interface import getter
from LbnlIon7350Interface import processor
from LbnlIon7350Interface import loader

from LbnlIon7350Interface.utils import utils

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
    root = os.path.dirname(os.path.realpath(__file__))
    getter.run_update(root, interval)

if __name__ == '__main__':
    main()
