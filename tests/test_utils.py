"""
Unit tests for utils.py
"""

import LbnlIon7350Interface.LbnlIon7350Interface.utils.utils as utils

def test_not_exists_dir():
    """
    Check that exists_dir returns False for nonexistent path
    """
    nonexistent = '~/blahblah/'
    assert not utils.exists_dir(nonexistent)

def test_exists_dir():
    """
    Check that exists_dir returns True for root directory.
    """
    existent = '/'
    assert utils.exists_dir(existent)

def test_exists_tmpdir(tmpdir):
    """
    Check that exists_dir returns True on a temporary directory.
    """
    path = tmpdir.mkdir('test_exists')
    assert utils.exists_dir(str(path))

def test_not_exists_file():
    """
    Check that exists_file returns False for nonexistent file
    """
    nonexistent = '~/blabjfajdfd'
    assert not utils.exists_file(nonexistent)

def test_exists_file(tmpdir):
    """
    Check that exists_file returns True for a temp file.
    The temp file is deleted after this test finishes.
    """
    existent = tmpdir.mkdir('test_file').join('dummy.txt')
    existent.write('hello world!')
    path = str(existent)
    assert utils.exists_file(path)
    assert not utils.exists_dir(path)

def test_get_cnxn_str(tmpdir):
    """
    Check that get_cnxn_str properly reads from a temporary credentials file
    and returns a correct login string.
    """
    cf = tmpdir.mkdir('test_get_cnxn_str').join('creds.txt')
    cf.write('user\npassword')
    cnxn_str = utils.get_cnxn_str(str(cf))
    assert cnxn_str == 'DSN=ION;UID=user;PWD=password'

