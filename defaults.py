"""
Contains default values for variables.
"""

import os

cwd = os.getcwd()

PROJECT = 'LbnlIon7350Interface'

# Directory to store downloaded meter reading data.
DOWNLOADS = os.path.join(cwd, 'downloaded_data')

# Directory to store generated json files for future push to BuildingOS.
JSON_DIR = os.path.join(cwd, 'json_dir')

# Read only file containing database login credentials
CREDS = os.path.join(cwd, PROJECT, '.ioninfo')

# File containing ION 7350 meter information
METER_FILE = os.path.join(cwd, PROJECT, 'ion7350meters.csv')

