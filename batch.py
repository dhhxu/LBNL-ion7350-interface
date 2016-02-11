"""
This is the batch script for the ION 7350 interface to BuildingOS. Requires the user to
pass start and end dates as strings. The script downloads reading data that occurs
between the two dates for each meter listed in an input csv file, packages it into a JSON
object as per Lucid's Connector API, and pushes that object to BuildingOS.

The dates are strings and must be in the following format:

    'YYYY-MM-DD HH:MM:SS'
"""

import os
import sys

from LbnlIon7350Interface import getter
from LbnlIon7350Interface import processor
from LbnlIon7350Interface import loader
from LbnlIon7350Interface.utils import utils

def _usage():
    string = "USAGE:\n\tpython batch.py [start date] [end date] [meter index]\n"
    print(string)

def main():
    if len(sys.argv) < 3:
        utils.error('Requires a start and end date')
        _usage()
        exit()
    start = sys.argv[1]
    end = sys.argv[2]
    idx = None
    if len(sys.argv) == 4:
        try:
            idx = int(sys.argv[3])
        except ValueError:
            utils.error("Index argument must be an integer")
            sys.exit(1)
    root = os.path.dirname(os.path.realpath(__file__))
    getter.run_batch(root, start, end, idx)
    processor.create_json(root)
    #loader.post_json_files(root)

if __name__ == '__main__':
    main()

