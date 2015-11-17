"""
Collection of utility methods.
"""

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

