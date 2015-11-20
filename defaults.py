"""
Contains default values for variables.
"""

import os

cwd = os.path.dirname(os.path.realpath(__file__))

PROJECT = 'LbnlIon7350Interface'

# Directory to store downloaded meter reading data.
DOWNLOADS = os.path.join(cwd, 'downloaded_data')

# Directory to store generated json files for future push to BuildingOS.
JSON_DIR = os.path.join(cwd, 'json_data')

# Read only file containing database login credentials
CREDS = os.path.join(cwd, PROJECT, '.ioninfo')

# File containing ION 7350 meter information
METER_FILE = os.path.join(cwd, PROJECT, 'ion7350meters.csv')

# Log directory
LOG_DIR = os.path.join(cwd, 'logs')

# File to hold logging data
LOG_FILE = os.path.join(LOG_DIR, 'ion7350interface.log')

# Default update interval frequency in hours
INTERVAL = 4

def test():
    from LbnlIon7350Interface.utils import utils
    paths = [cwd, DOWNLOADS, JSON_DIR, CREDS, METER_FILE, LOG_FILE]

    for path in paths:
        if not utils.exists_dir(path) and not utils.exists_file(path):
            utils.error('Path does not exist: %s' % (path))
        else:
            print('Path exists: %s' % (path))

if __name__ == '__main__':
    test()

