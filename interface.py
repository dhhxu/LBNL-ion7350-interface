#!/usr/bin/env python

"""
This is the updater script for the ION 7350 interface to BuildingOS. Every X hours, where
X is some number between 2 and 12 (larger intervals are not good), downloads reading data
from the past X hours for each meter listed in an input csv file, packages it into a JSON
object as per Lucid's Connector API, and pushes that object to BuildingOS.
"""

import getter
import processor
import loader

def main():
    pass

if __name__ == '__main__':
    main()
