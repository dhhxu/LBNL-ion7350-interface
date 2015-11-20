import LbnlIon7350Interface.LbnlIon7350Interface.utils.utils as utils

from os import remove

def test_exists_dir():
    nonexistent = '~/blahblah/'
    assert not utils.exists_dir(nonexistent)

    existent = '/home/daniel/Downloads/'
    assert utils.exists_dir(existent)

def test_exists_file():
    nonexistent = '~/blabjfajdfd'
    assert not utils.exists_file(nonexistent)
    existent = 'dummy.txt'
    with open(existent, 'wb') as f:
        f.write('hello world!')
        assert utils.exists_file(existent)
        assert not utils.exists_dir(existent)
    remove(existent)
