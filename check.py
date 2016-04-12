"""
This is the script that prints the earliest and latest reading timestamp for
each meter in the meter csv file.

If a meter in the file does not exist in the ION database, 'None' will be
displayed.
"""

import os
import pyodbc

from LbnlIon7350Interface.utils import utils
from LbnlIon7350Interface.utils import defaults
from LbnlIon7350Interface.utils import Cursor

def get_query_str(asc):
    """
    Return the SQL query string that will get the earliest or latest timestamp
    that exists for a given meter name and QuantityID.

    If asc is True, get earliest timestamp. Otherwise, get latest timestamp.

    To use the query string, the user needs to specify two (2) parameters
    when passing the string to cursor.execute():
        name string
        qid integer
    Params:
        asc boolean
    """
    option = 'ASC'
    if not asc:
        option = 'DESC'

    query = '''SELECT TOP 1 D.TimestampUTC
     FROM ION_Data.dbo.DataLog2 D
     INNER JOIN ION_Data.dbo.Source S
     ON S.ID = D.SourceID
     AND S.Name = ?
     AND D.QuantityID = ?
     ORDER BY D.TimestampUTC %s''' % (option)
    return query

def get_timestamps(cursor, meters, query):
    """
    For each meter in meters list, execute SQL query using existing cursor
    object.

    Returns a dictionary where keys are meter ION names and values are
    earliest or latest timestamps, depending on query's contents.

    Params:
        cursor: Cursor object
        meters: list of meter rows
        query: string
    """
    output = {}
    for m in meters:
        ion_name = utils.get_ion_name(m)
        qid = utils.get_ion_qid(m)
        try:
            cursor.execute(query, ion_name, qid)
        except pyodbc.Error:
            pass
        if cursor.rowcount == 0:
            output[ion_name] = None
            continue
        row = cursor.fetchone()
        ts = row.TimestampUTC.split(".")[0]
        output[ion_name] = ts

    return output

def run(root):
    creds_file = defaults.creds(root)
    cnxn_str = utils.get_cnxn_str(creds_file)
    meter_file = defaults.meter_file(root)

    earliest = {}
    latest = {}
    print("Running check.py...")
    with Cursor.Cursor(cnxn_str) as cursor:
        earliest_query = get_query_str(True)
        latest_query = get_query_str(False)
        meter_generator = utils.read_meter_file(meter_file)
        meters = [m for m in meter_generator]
        earliest = get_timestamps(cursor, meters, earliest_query)
        latest = get_timestamps(cursor, meters, latest_query)

        for m in meters:
            ion_name = utils.get_ion_name(m)
            earliest_ts = earliest[ion_name]
            latest_ts = latest[ion_name]
            print("%s\tStart: %s\tEnd: %s" % (ion_name, earliest_ts, latest_ts))

def main():
    root = os.path.dirname(os.path.realpath(__file__))
    run(root)


if __name__ == '__main__':
    main()
