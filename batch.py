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
import LbnlIon7350Interface.getter
import LbnlIon7350Interface.processor
import LbnlIon7350Interface.loader

from LbnlIon7350Interface.utils import utils
from LbnlIon7350Interface.utils import read_creds
from LbnlIon7350Interface.utils import Cursor
from LbnlIon7350Interface.utils import defaults

def _usage():
    string = "USAGE:\n\tpython batch.py [start date] [end date]\n"
    print(string)

def main():
    if len(sys.argv) < 3:
        utils.error('Requires a start and end date')
        _usage()
        exit()
    start = sys.argv[1]
    end = sys.argv[2]
    root = os.path.dirname(os.path.realpath(__file__))
    getter.run_batch(root, start, end)

if __name__ == '__main__':
    main()

    # root = os.path.dirname(os.path.realpath(__file__))
    # print(root)
    # gen = utils.read_meter_file(defaults.meter_file(root))
    # for row in gen:
    #     mid, name = utils.get_lucid_name_and_id(row)
    #     print("id: %s | name: %s" % (mid, name))
    #     date = utils.get_last_reading_date(row)



