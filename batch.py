"""
This is the batch script for the ION 7350 interface to BuildingOS. Requires the user to
pass start and end dates as strings. The script downloads reading data that occurs
between the two dates for each meter listed in an input csv file, packages it into a JSON
object as per Lucid's Connector API, and pushes that object to BuildingOS.

The dates are strings and must be in the following format:

    'YYYY-MM-DD HH:MM:SS'
"""

import sys
import LbnlIon7350Interface.getter
import LbnlIon7350Interface.processor
import LbnlIon7350Interface.loader
import defaults

from LbnlIon7350Interface.utils.utils import error
from LbnlIon7350Interface.utils import read_creds
from LbnlIon7350Interface.utils import Cursor

def get_cnxn_str():
    """
    Returns a connection string that enables logging into the ION database.
    """
    user, pwd = read_creds.read(defaults.CREDS)
    cnxn_str = 'DSN=ION;UID=%s;PWD=%s' % (user, pwd)
    return cnxn_str

def _usage():
    string = "USAGE:\n\tpython batch.py [start date] [end date]\n"
    print(string)

def main():
    if len(sys.argv) < 3:
        error('Requires a start and end date')
        _usage()
        exit()
    start = sys.argv[1]
    end = sys.argv[2]

if __name__ == '__main__':
    main()
