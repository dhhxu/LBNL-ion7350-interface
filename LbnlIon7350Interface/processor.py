"""
Processor script.

Takes as input a directory containing downloaded reading data files. These files
are in csv format.

This script returns a JSON file containing the data from the data files in the
input directory. The JSON file is saved to a designated json directory.

Initially, the JSON file is empty. The script reads each csv file in the download
directory and appends the data to the JSON file.

When all csv files are read and the JSON file is created, the csv files are
archived in a designated data archive.

The JSON file conforms to the format dictated by the Lucid BuildingOS API.
"""

import csv
import json
import os

from datetime import datetime

from utils import defaults
from utils import utils


def create_json(root):
    """
    Create the json file containing reading data.

    Params:
        root string
    """
    data_dir = defaults.downloads(root)
    output_dir = defaults.json_dir(root)
    archive = defaults.data_archive(root)

    catalog = []
    data = []
    json_file = {}

    data_files = utils.get_files_in_dir(data_dir)
    if not data_files:
        utils.warn('No csv files to process. Terminating')
        exit()

    utils.print_time('PROCESSOR START')
    print('Begin JSON file generation')
    for data_file in data_files:
        with open(data_file, 'rb') as f:
            reader = csv.reader(f)
            meterId, meterName = reader.next()

            print('Processing meterId %s ...' % (meterId)),

            info = {'meterId': meterId, 'meterName': meterName}
            catalog.append(info)

            for row in reader:
                ts = row[0]
                val = float(row[1])
                reading = {'timestamp': ts,
                           'value': val,
                           'meterId': meterId}
                data.append(reading)

            print('done')
        utils.move(data_file, archive)

    json_file['datasource'] = defaults.URI
    json_file['meterCatalog'] = catalog
    json_file['readings'] = data

    print('End JSON file generation')

    curr_dt = datetime.now()
    json_fname = 'dump_%s.json' % (utils.format_dt(curr_dt))
    save_path = os.path.join(output_dir, json_fname)

    print('Writing JSON to file %s ...' % (save_path)),
    with open(save_path, 'wb') as out:
        json.dump(json_file, out)
        print('done')

    utils.print_time('PROCESSOR END')

