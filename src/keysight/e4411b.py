# -*- coding: utf-8 -*-
# Copyright (c) 2013-2022 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Read a CSV file saved by an E4411B Spectrum Analyzer
"""

# Standard module imports
import csv
import sys

# Data analysis related imports
import numpy as np


def read_csv_file(filename):
    """Read csv file into a numpy array
    """
    header_info = {}
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
        temp_row = mynext()
        header_info['timestamp'] = temp_row[0]
        header_info['file'] = temp_row[1]
        header_info['title'] = mynext()[1]
        header_info['model'] = mynext()[1]
        header_info['serial_number'] = mynext()[1]
        temp_row = mynext()
        header_info['center_freq'] = float(temp_row[1])
        temp_row = mynext()
        header_info['span_freq'] = float(temp_row[1])
        temp_row = mynext()
        header_info['resolution_bw'] = float(temp_row[1])
        temp_row = mynext()
        header_info['video_bw'] = float(temp_row[1])
        temp_row = mynext()
        header_info['ref_level'] = float(temp_row[1])
        temp_row = mynext()
        header_info['sweep_time'] = float(temp_row[1])
        temp_row = mynext()
        header_info['num_points'] = int(temp_row[1])
        temp_row = mynext()  # Skip blank line 12
        temp_row = mynext()  # Skip blank line 13
        temp_row = mynext()
        num_traces = len(temp_row) - 1
        header_info['num_traces'] = num_traces
        temp_row = mynext()
        header_info['frequency'] = temp_row[0]

        data_array = []

        if num_traces == 1:
            for row in data:
                data_array.append((float(row[0]), float(row[1])))
            data = np.array(
                data_array,
                dtype={'names': ('frequency', 'amplitude'),
                       'formats': ('f8', 'f8')})
        elif num_traces == 2:
            for row in data:
                data_array.append((float(row[0]),
                                   [float(row[1]),
                                   float(row[2])]))
            data = np.array(
                data_array,
                dtype={'names': ('frequency', 'amplitude'),
                       'formats': ('f8', '2f8')})
        elif num_traces == 3:
            for row in data:
                data_array.append((float(row[0]),
                                   [float(row[1]),
                                   float(row[2]),
                                   float(row[3])]))
            data = np.array(
                data_array,
                dtype={'names': ('frequency', 'amplitude'),
                       'formats': ('f8', '3f8')})

    return (header_info, data)
