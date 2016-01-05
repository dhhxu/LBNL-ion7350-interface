"""
Setup script

The ION 7350 interface requires several directories and files to work. If the
interface is to be run on a different machine, run this script to set up the
requisite directories and files.
"""

import os
from getpass import getpass

from LbnlIon7350Interface.utils import defaults
from LbnlIon7350Interface.utils import utils

def safe_mkdir(path):
    """
    Creates a directory at path, if it doesn't exist already.

    If path already exists, does nothing. Raises a ValueError
    if path is not a valid directory name.

    Params:
        path string
    """
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise ValueError('Bad directory name')

def get_username():
    """
    Prompt user for username. Returns the entered name.
    """
    return raw_input("Username: ")

def get_password():
    """
    Prompt user for password. The user will enter password twice.

    If the passwords don't match, keep retrying. The method can be
    interrupted; it is responsibility of the caller to handle this
    interrupt.

    Returns the entered password.
    """
    while True:
        pass1 = getpass("Password: ")
        pass2 = getpass("Enter password again: ")
        if not pass1 or not pass2:
            print('No password entered. Please try again.')
            continue
        elif pass1 != pass2:
            print('Passwords do not match. Pease try again.')
            continue
        elif pass1 == pass2:
            return pass1

def make_creds_file(root):
    """
    Prompt the user for user name and password to create a read-only file
    containing login credentials. If the user cancels the operation anytime,
    raises an IOError and no file is created.

    root is the root directory of the interface program. It is needed so that
    the credentials file is saved in the correct location.

    The file contains two lines. The first is username. The second is password.

    Params:
        root string
    """
    path = defaults.creds(root)
    if utils.exists_file(path):
        while True:
            answer = raw_input('Credentials file found. Do you want to overwrite (Y/N)? ')
            if answer.lower() == 'y':
                os.remove(path)
                break
            elif answer.lower() == 'n':
                return
            else:
                print('Unknown input. Please try again.')

    try:
        user = get_username()
        pwd = get_password()
    except KeyboardInterrupt:
        raise IOError('User cancelled operation')

    with open(path, 'wb') as cf:
        cf.write('%s\n' % (user))
        cf.write(pwd)
    os.chmod(path, 0400)


def main():
    root = os.path.dirname(os.path.realpath(__file__))
    try:
        safe_mkdir(os.path.join(root, 'downloaded_data/archive'))
        safe_mkdir(os.path.join(root, 'json_data/archive'))
        make_creds_file(root)
    except ValueError as err:
        utils.error(str(err))
    except IOError as ierr:
        utils.error(str(ierr))

if __name__ == '__main__':
    main()
