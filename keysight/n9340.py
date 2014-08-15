# -*- coding: utf-8 -*-
# Copyright (c) 2013 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Read a CSV file saved by an N9340 Spectrum Analyzer
"""

# Try to future proof code so that it's Python 3.x ready
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

# Standard module imports
import csv

# Data analysis related imports
import numpy as np


def read_csv_file(filename):
    """Read csv file into a numpy array
    """
    n9340_header = {}
    with open(filename, 'rb') as csvfile:
        data = csv.reader((line.replace(b'\0', b'') for line in csvfile),
                          delimiter=b',')
        n9340_header['file'] = data.next()[1]
        n9340_header['system_parameter'] = data.next()[1]
        temp_row = data.next()
        n9340_header['ref'] = float(temp_row[1])
        n9340_header['ref_offset'] = float(temp_row[3])
        temp_row = data.next()
        n9340_header['start_freq'] = float(temp_row[1])
        n9340_header['stop_freq'] = float(temp_row[3])
        temp_row = data.next()
        n9340_header['center_freq'] = float(temp_row[1])
        n9340_header['span_freq'] = float(temp_row[3])
        temp_row = data.next()
        n9340_header['vbw'] = float(temp_row[1])
        n9340_header['vbw_mode'] = temp_row[2]
        n9340_header['rbw'] = float(temp_row[4])
        n9340_header['rbw_mode'] = temp_row[5]
        temp_row = data.next()
        n9340_header['vbw_to_rbw'] = float(temp_row[1])
        n9340_header['vbw_to_rbw_mode'] = temp_row[2]
        n9340_header['sweep_time'] = float(temp_row[4])
        n9340_header['sweep_time_mode'] = temp_row[5]
        temp_row = data.next()
        n9340_header['attenuation'] = float(temp_row[1])
        n9340_header['attenuation_mode'] = temp_row[2]
        temp_row = data.next()
        n9340_header['scale_div'] = float(temp_row[1])
        n9340_header['scale_type'] = temp_row[3]
        n9340_header['preamp'] = temp_row[5]
        temp_row = data.next()
        n9340_header['psd_mode'] = temp_row[1]
        temp_row = data.next()
        temp_row = data.next()
        # FIXME(mdr) Use a regex or something better than this
        n9340_header['trace_unit'] = temp_row[0].split(':')[2][:-1]
        temp_row = data.next()
        n9340_header['frequency'] = temp_row[0]

        n9340_array = []

        for row in data:
            n9340_array.append((float(row[0]), float(row[1])))

        n9340_data = np.array(
            n9340_array,
            dtype={'names': ('frequency', 'amplitude_db'),
                   'formats': ('f8', 'f8')})

    return (n9340_header, n9340_data)
