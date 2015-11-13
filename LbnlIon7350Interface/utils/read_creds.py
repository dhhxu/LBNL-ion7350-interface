"""
This method reads login credentials from a read-only file.
The input file must have two lines: username and password.
Additional lines will be ignored.
"""

def read(infile):
    """
    Returns a list where the first element is the username string,
    the second the password string.
    If an error occurs, returns None.
    """
    try:
        with open(infile, 'r') as f:
            creds = list(f)
            if len(creds) < 2:
                return None
            return [elem.strip() for elem in creds[:2]]
    except IOError:
        return None

