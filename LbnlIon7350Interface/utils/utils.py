"""
Collection of utility methods.
"""

import csv
import os
import re
import read_creds
import defaults

def error(msg):
    """
    Print msg with [ERROR] appended.

    Params:
        msg string
    """
    print('[ERROR] %s' % (msg))

def warn(msg):
    """
    Print msg with [WARN] appended.

    Params:
        msg string
    """
    print('[WARN] %s' % (msg))

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

def get_cnxn_str(path):
    """
    Returns a connection string that enables logging into the ION database. The
    file containing login information must be located at path.
    """
    user, pwd = read_creds.read(path)
    cnxn_str = 'DSN=ION;UID=%s;PWD=%s' % (user, pwd)
    return cnxn_str

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

def get_ion_name(row):
    """
    Return the meter name in the ION database.

    Params:
        row list [type, name, quantity id, date]
    """
    return row[1]

def get_ion_qid(row):
    """
    Return the quantity ID for the meter in the ION database.

    Params:
        row list [type, name, quantity id, date]
    """
    return int(row[2])

def get_last_reading_date(row):
    """
    Returns the date of the most recent pulled data for the meter described by
    the input row. If there is no date, return None instead.

    This is used to help avoid downloading duplicate data; i.e. downloading data that
    is already in BuildingOS.

    Params:
        row list [type, name, quantity id, date]
    """
    date = row[-1]
    if not date:
        date = None

    return date

def get_lucid_id_and_name(row):
    """
    Returns a tuple containing the id and name (in that order) that will be
    associated with the meter in the input row.

    The name and id are deterministic and rely on the meter's ION name having
    the form:

        LBL_ION_##.BLDG_ROOM

    Params:
        row list [type, name, quantity id, date]
    """
    comm = row[0]
    name = row[1]
    meterId = "_".join([name, comm])
    pstr = r'\.(.*)'
    m = re.search(pstr, name)
    if not m:
        raise ValueError('Invalid ION meter name')
    bldg_info = m.group(1)

    meterName = "".join(['bldg', bldg_info])
    return meterId, meterName

def make_lucid_ts(ts):
    """
    Convert the timestamp returned by a query on the ION database into a
    format specified by the Lucid API.

    Params:
        ts string
    """
    parts = ts.split()
    joined = "T".join(parts)
    parts = joined.split(".")
    return parts[0]

def round_down(dt):
    """
    Rounds the datetime object to the nearest hour (seconds are truncated).

    Params:
        dt datetime object
    """
    return dt.replace(minute=0, second=0)

def format_dt(dt):
    """
    Return the string representation of the datetime object in Lucid formato

    Params:
        dt datetime object.
    """
    return dt.strftime('%Y-%m-%dT%H:%M:%S')

def get_files_in_dir(path):
    """
    Return a list of absolute paths to files in the directory at path.

    Directories are excluded.

    Params:
        path string
    """
    files = [os.path.join(path, f) for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))]
    return files


if __name__ == '__main__':
    pass
