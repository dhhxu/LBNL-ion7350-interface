"""
Getter script.

Takes as input a csv file containing ION 7350 meters to get reading data for.
For each meter, downloads reading data into a csv file. The downloaded files
are saved in a designated downloads directory.

The data is located in the ION database; login credentials are required.

The script is intended to be used in two ways: batch and update.

In batch mode, the script takes a start date and end date parameters. Reading
data that have timestamps between the two dates will be retrieved. This mode
is intended for one-time usage for loading historical data.

In update mode, the script takes an interval parameter. It will download
reading data with timestamps that occur within the last interval hours
of the script execution. This mode is intended to be used when new data
needs to be fetched periodically.
"""



from datetime import datetime

from utils import utils
from utils import read_creds
from utils import Cursor

def is_valid_interval(interval):
    """
    Returns true if interval is an positive integer and is not too large.

    Params:
        interval integer
    """
    if not isinstance(interval, (int, long)):
        return False
    elif interval < 2 or interval > 12:
        return False
    else:
        return True


def get_date(date):
    """
    Returns the datetime object representing the date string. If date is
    malformed, return None instead.

    date is formatted as follows:
        YYYY-MM-DD HH:MM:SS

    Params:
        date string
    """
    try:
        date_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return date_object
    except ValueError:
        return None


def run_batch(output_dir, start, end):
    """
    Run this script in batch mode. Download reading data whose timestamps
    lie within start and end dates into output_dir.

    The date must follow the following format:
        YYYY-MM-DD HH:MM:SS

    where 24 hour time is used.

    Params:
        output_dir string
        start string
        end string
    """
    s_date = get_date(start)
    e_date = get_date(end)

    if not s_date or not e_date:
        utils.error('Invalid/missing dates')
        return
    elif start > end:
        utils.error('Start date must come before end date')
        return
    elif not utils.exists_dir(output_dir):
        utils.error('Output directory not found')
        return

def run_update(output_dir, interval):
    pass

def test():
    start = '2012-11-01 00:15:00'
    end = '2014-01-01 12:34:00'
    s = get_date(start)
    e = get_date(end)
    print(s)
    print(e)
    ns = s.replace(minute=0, second=0)
    print(ns)
    ne = e.replace(minute=0, second=0)
    print(ne)

if __name__ == '__main__':
    test()

