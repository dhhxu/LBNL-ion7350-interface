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

import csv
import os
import pyodbc

from datetime import datetime, timedelta

from utils import defaults
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

    date is formatted as follows (note the T between date and time):
        YYYY-MM-DDTHH:MM:SS

    Params:
        date string
    """
    try:
        date_object = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
        return date_object
    except ValueError:
        return None

def get_source_query(name):
    """
    Return the SQL query string that will get the ID associated with the meter name.

    Params:
        name string
    """
    query = '''SELECT TOP 1 ID FROM
    ION_Data.dbo.Source
    WHERE Name = '%s';''' % (name)
    return query

def get_query_str(sid, qid, start, end):
    """
    Return the SQL query string that will get reading data for a given meter ID and
    QuantityID in a date range.

    Params:
        sid integer
        qid integer
        start string
        end string
    """
    query = '''SELECT TOP 1 TimestampUTC, Value FROM
     ION_Data.dbo.DataLog2
     WHERE SourceID = %d AND QuantityID = %d
     AND TimestampUTC >= '%s' AND TimestampUTC < '%s';''' % (sid, qid, start, end)
    return query

def run_batch(root, start, end):
    """
    Run this script in batch mode. Download reading data whose timestamps
    lie within start and end dates.

    The date must follow the following format (Note the T between date and time):
        YYYY-MM-DDTHH:MM:SS

    where 24 hour time is used.

    Params:
        root string
        start string
        end string
    """
    s_date = get_date(start)
    e_date = get_date(end)

    if not s_date or not e_date:
        raise ValueError('Invalid/missing dates')
    elif start > end:
        raise ValueError('Start date must come before end date')
    elif not utils.exists_dir(root):
        raise ValueError('Root directory not found')

    creds_file = defaults.creds(root)
    cnxn_str = utils.get_cnxn_str(creds_file)
    output_dir = defaults.downloads(root)
    meter_file = defaults.meter_file(root)

    with Cursor.Cursor(cnxn_str) as cursor:

        meters = utils.read_meter_file(meter_file)
        for m in meters:
            ion_name = utils.get_ion_name(m)
            qid = utils.get_ion_qid(m)
            src_query = get_source_query(ion_name)

            try:
                cursor.execute(src_query)
            except pyodbc.Error:
                utils.error('Failed to get ID for meter %s' % (ion_name))
                continue

            result = cursor.fetchone()
            if not result:
                utils.error('Meter %s does not exist' % (ion_name))
                continue

            sid = result.ID
            data_query = get_query_str(sid, qid, str(s_date), str(e_date))
            try:
                cursor.execute(data_query)
            except pyodbc.Error:
                utils.error('Failed to get data for meter %s qid %d' % (ion_name, qid))
                continue
            if not cursor:
                utils.warn('No data found for meter %s qid %d' % (ion_name, qid))
                continue

            meterId, meterName = utils.get_lucid_id_and_name(m)
            dl_fname = "%sT%s.csv" % (meterId, utils.make_lucid_ts(str(s_date)))
            path = os.path.join(output_dir, dl_fname)

            print('Writing data for meter %s qid %d to file: %s ...' % (ion_name, qid, path)),
            with open(path, 'wb') as data_file:
                writer = csv.writer(data_file)
                writer.writerow([meterId, meterName])

                for row in cursor:
                    ts = row.TimestampUTC
                    val = row.Value
                    data_row = [utils.make_lucid_ts(ts), val]
                    writer.writerow(data_row)
                print('done')

            break

def run_update(root, interval):
    """
    Run this script in update mode. Download reading data whose timestamps
    lie within now - interval and now dates.

    Interval must be a positive integer between 2 and 12.

    Params:
        root string
        output_dir string
        interval integer
    """
    if not is_valid_interval(interval):
        raise ValueError('Invalid interval')

    curr_dt = datetime.now()
    curr_dt = utils.round_down(curr_dt)
    prev_dt = curr_dt - timedelta(hours=interval)
    run_batch(root, utils.format_dt(prev_dt), utils.format_dt(curr_dt))

def test():
    start = '2012-11-01T00:15:00'
    end = '2014-01-01T12:34:00'
    s = get_date(start)
    e = get_date(end)
    print(s)
    print(e)
    ns = s.replace(minute=0, second=0)
    print(ns)
    ne = e.replace(minute=0, second=0)
    print(ne)

    # print(defaults.INTERVAL)

if __name__ == '__main__':
    test()
