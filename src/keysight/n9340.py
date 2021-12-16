# -*- coding: utf-8 -*-
# Copyright (c) 2013-2022 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Read a CSV file saved by an N9340 Spectrum Analyzer
"""

# Standard module imports
import csv
import re
import sys

# Data analysis related imports
import numpy as np


def read_csv_file(filename):
    """Read csv file into a numpy array
    """
    n9340_header = {}
    # Make this Py2.x and Py3.x compatible
    if sys.version_info[0] < 3:
        infile = open(filename, 'rb')
    else:
        infile = open(filename, 'r', newline='', encoding='utf8')

    with infile as csvfile:
        # Make this Py2.x and Py3.x compatible
        if sys.version_info[0] < 3:
            data = csv.reader((line.replace(b'\0', b'') for line in csvfile),
                              delimiter=b',')
            mynext = data.next
        else:
            data = csv.reader((line.replace('\0', '') for line in csvfile),
                              delimiter=',')
            mynext = data.__next__
        n9340_header['file'] = mynext()[1]
        n9340_header['system_parameter'] = mynext()[1]
        temp_row = mynext()
        n9340_header['ref'] = _get_ref(temp_row[1])
        n9340_header['ref_offset'] = float(temp_row[3])
        temp_row = mynext()
        n9340_header['start_freq'] = float(temp_row[1])
        n9340_header['stop_freq'] = float(temp_row[3])
        temp_row = mynext()
        n9340_header['center_freq'] = float(temp_row[1])
        n9340_header['span_freq'] = float(temp_row[3])
        temp_row = mynext()
        n9340_header['vbw'] = float(temp_row[1])
        n9340_header['vbw_mode'] = temp_row[2]
        n9340_header['rbw'] = float(temp_row[4])
        n9340_header['rbw_mode'] = temp_row[5]
        temp_row = mynext()
        n9340_header['vbw_to_rbw'] = float(temp_row[1])
        n9340_header['vbw_to_rbw_mode'] = temp_row[2]
        n9340_header['sweep_time'] = float(temp_row[4])
        n9340_header['sweep_time_mode'] = temp_row[5]
        temp_row = mynext()
        n9340_header['attenuation'] = float(temp_row[1])
        n9340_header['attenuation_mode'] = temp_row[2]
        temp_row = mynext()
        n9340_header['scale_div'] = float(temp_row[1])
        n9340_header['scale_type'] = temp_row[3]
        n9340_header['preamp'] = temp_row[5]
        temp_row = mynext()
        n9340_header['psd_mode'] = temp_row[1]
        temp_row = mynext()
        temp_row = mynext()
        if temp_row[0] == 'Marker':
            # File has a marker, so skip that for now.
            temp_row = mynext()
            temp_row = mynext()
            temp_row = mynext()
        # FIXME(mdr) Use a regex or something better than this
        n9340_header['trace_unit'] = temp_row[0].split(':')[2][:-1]
        temp_row = mynext()
        n9340_header['frequency'] = temp_row[0]

        n9340_array = []

        for row in data:
            n9340_array.append((float(row[0]), float(row[1])))

        n9340_data = np.array(
            n9340_array,
            dtype={'names': ('frequency', 'amplitude_db'),
                   'formats': ('f8', 'f8')})

    return (n9340_header, n9340_data)


def _get_ref(s):
    """Convert given string into the reference level
    """
    match = re.search(r'[\d.]+', s)
    if match:
        return float(match.group())
    else:
        return ''
