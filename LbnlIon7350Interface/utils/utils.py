"""
Collection of utility methods.
"""

import csv
import os

def error(msg):
    """
    Print msg with [ERROR] appended.
    """

    print('[ERROR] %s' % (msg))


def exists_dir(path):
    """
    Returns true if path exists.

    Params:
        path string
    """
    return os.path.isdir(path)

def exists_file(path):
    """
    Returns true if file at path path exists.

    Params:
        path string
    """
    return os.path.isfile(path)

def read_meter_file(path):
    """
    Returns a generator for the csv file containing meter information.

    Params:
        path string
    """
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            yield row



