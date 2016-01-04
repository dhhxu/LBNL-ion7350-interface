"""
Unit tests for utils.py
"""

from os import remove

import LbnlIon7350Interface.LbnlIon7350Interface.utils.utils as utils

def test_not_exists_dir():
    """
    Check that exists_dir returns False for nonexistent path
    """
    nonexistent = '~/blahblah/'
    assert not utils.exists_dir(nonexistent)

def test_exists_dir():
    """
    Check that exists_dir returns True for valid path
    """
    existent = '/'
    assert utils.exists_dir(existent)

def test_not_exists_file():
    """
    Check that exists_file returns False for nonexistent file
    """
    nonexistent = '~/blabjfajdfd'
    assert not utils.exists_file(nonexistent)

def test_exists_file():
    """
    Check that exists_file returns True for a temp file.
    The temp file is deleted after this test finishes.
    """
    existent = 'dummy.txt'
    with open(existent, 'wb') as f:
        f.write('hello world!')
        assert utils.exists_file(existent)
        assert not utils.exists_dir(existent)
        remove(existent)

def test_get_cnxn_str():
    """
    Check that get_cnxn_str properly reads from a temporary credentials file
    and returns a correct login string.
    """
    tmp = 'creds.txt'
    with open(tmp, 'wb') as cf:
        cf.write('user\n')
        cf.write('password')
    cnxn_str = utils.get_cnxn_str(tmp)
    assert cnxn_str == 'DSN=ION;UID=user;PWD=password'

    remove(tmp)

