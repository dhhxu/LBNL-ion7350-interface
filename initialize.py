"""
This is the initialize script for the ION 7350 interface to BuildingOS. Takes no
arguments. The script parses an input csv file containing meter information
and produces a JSON containing a meter catalog containing information about
the meters.

This script must be run whenever there is a change to the 7350 meter configuration;
i.e. new meters are added. This step is necessary because a meter must have its
corresponding point already established in BuildingOS before the system can begin
to accept readings from that meter. Otherwise, any readings for that meter will
not be accepted by BuildingOS.
"""

import json
import os
from datetime import datetime

from LbnlIon7350Interface import loader

from LbnlIon7350Interface.utils import utils
from LbnlIon7350Interface.utils import defaults

def create_catalog(root):
    """
    Create a json file containing the meter catalog from the meter file.
    The file is saved to the json directory.

    Params:
        root string
    """
    meter_file = defaults.meter_file(root)
    output_dir = defaults.json_dir(root)
    catalog = []
    json_file = {}

    meters = utils.read_meter_file(meter_file)
    for m in meters:
        meterId, meterName = utils.get_lucid_id_and_name(m)
        info = {'meterId': meterId, 'meterName': meterName}
        catalog.append(info)

    json_file['datasource'] = defaults.URI
    json_file['meterCatalog'] = catalog
    json_file['readings'] = []

    curr_dt = datetime.now()
    json_fname = 'catalog_%s.json' % (utils.format_dt(curr_dt))
    save_path = os.path.join(output_dir, json_fname)

    with open(save_path, 'wb') as out:
        json.dump(json_file, out)

def main():
    root = os.path.dirname(os.path.realpath(__file__))
    create_catalog(root)
    loader.post_json_files(root)

if __name__ == '__main__':
    main()

