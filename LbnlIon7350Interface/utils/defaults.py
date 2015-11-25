"""
Contains default values for variables.
"""

import os

cwd = os.path.dirname(os.path.realpath(__file__))

PROJECT = 'LbnlIon7350Interface'

def downloads(root):
    """
    Returns the directory containing downloaded data. Root is the project
    root directory.
    """
    return os.path.join(root, 'downloaded_data')

def json_dir(root):
    """
    Returns the directory containing the processed JSON data. Root is the
    project root directory
    """
    return os.path.join(root, 'json_data')

def creds(root):
    """
    Returns the path to the ION database credentials file. Root is the
    project root directory.
    """
    return os.path.join(root, PROJECT, '.ioninfo')

def meter_file(root):
    """
    Returns the path to the csv file containing ION 7350 meter information.
    Root is the project root directory.
    """
    return os.path.join(root, PROJECT, 'ion7350meters.csv')

def log_dir(root):
    """
    Returns the path to the directory containing logs. Root is the project
    root directory.
    """
    return os.path.join(root, 'logs')

def log_file(root):
    """
    Returns the path to the primary log file for this interface. Root is the
    project root directory.
    """
    return os.path.join(root, 'logs', 'ion7350interface.log')

# Default update interval frequency in hours
INTERVAL = 4

def test():
    import utils
    root = '/home/daniel/work/LbnlIon7350Interface/'
    paths = [downloads, json_dir, creds, meter_file, log_file]

    for path in paths:
        p = path(root)
        if not utils.exists_dir(p) and not utils.exists_file(p):
            utils.error('Path does not exist: %s' % (p))
        else:
            print('Path exists: %s' % (p))

if __name__ == '__main__':
    test()

