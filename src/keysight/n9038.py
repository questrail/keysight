# -*- coding: utf-8 -*-
# Copyright (c) 2013-2022 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Read a CSV file saved by an N9038 EMI Test Receiver
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
        header_info['data_file_type'] = temp_row[0]
        temp_row = mynext()
        temp_row = mynext()
        header_info['instrument_ver'] = temp_row[0]
        header_info['model_num'] = temp_row[1]
        temp_row = mynext()
        temp_row = mynext()
        temp_row = mynext()
        header_info['num_points'] = float(temp_row[1])
        temp_row = mynext()
        header_info['sweep_time'] = float(temp_row[1])
        temp_row = mynext()
        header_info['start_freq'] = float(temp_row[1])
        temp_row = mynext()
        header_info['stop_freq'] = float(temp_row[1])
        temp_row = mynext()
        header_info['average_count'] = float(temp_row[1])
        temp_row = mynext()
        header_info['average_type'] = temp_row[1]
        temp_row = mynext()
        header_info['rbw'] = float(temp_row[1])
        temp_row = mynext()
        header_info['rbw_filter'] = temp_row[1]
        temp_row = mynext()
        header_info['rbw_filter_bw'] = temp_row[1]
        temp_row = mynext()
        header_info['vbw'] = float(temp_row[1])
        temp_row = mynext()
        header_info['sweep_type'] = temp_row[1]
        temp_row = mynext()
        header_info['x_axis_scale'] = temp_row[1]
        temp_row = mynext()
        header_info['preamp_state'] = temp_row[1]
        temp_row = mynext()
        header_info['preamp_band'] = temp_row[1]
        temp_row = mynext()
        header_info['trigger_source'] = temp_row[1]
        temp_row = mynext()
        header_info['trigger_level'] = float(temp_row[1])
        temp_row = mynext()
        header_info['trigger_slope'] = temp_row[1]
        temp_row = mynext()
        header_info['trigger_delay'] = float(temp_row[1])
        temp_row = mynext()
        header_info['phase_noise_optimization'] = temp_row[1]
        temp_row = mynext()
        header_info['swept_if_gain'] = temp_row[1]
        temp_row = mynext()
        header_info['fft_if_gain'] = temp_row[1]
        temp_row = mynext()
        header_info['rf_coupling'] = temp_row[1]
        temp_row = mynext()
        header_info['fft_width'] = float(temp_row[1])
        temp_row = mynext()
        header_info['ext_ref'] = float(temp_row[1])
        temp_row = mynext()
        header_info['input'] = temp_row[1]
        temp_row = mynext()
        header_info['rf_calibration'] = temp_row[1]
        temp_row = mynext()
        header_info['attenuation'] = float(temp_row[1])
        temp_row = mynext()
        header_info['ref_level_offset'] = float(temp_row[1])
        temp_row = mynext()
        header_info['external_gain'] = float(temp_row[1])
        temp_row = mynext()
        header_info['trace_type'] = temp_row[1]
        temp_row = mynext()
        header_info['detector'] = temp_row[1]
        temp_row = mynext()
        header_info['trace_math'] = temp_row[1:len(temp_row)]
        temp_row = mynext()
        header_info['trace_math_oper1'] = temp_row[1:len(temp_row)]
        temp_row = mynext()
        header_info['trace_math_oper2'] = temp_row[1:len(temp_row)]
        temp_row = mynext()
        header_info['trace_math_offset'] = float(temp_row[1])
        temp_row = mynext()
        header_info['normalize'] = temp_row[1]
        temp_row = mynext()
        num_traces = len(temp_row) - 1
        header_info['num_traces'] = num_traces
        header_info['trace_name'] = temp_row[1:len(temp_row)]
        temp_row = mynext()
        header_info['x_axis_units'] = temp_row[1]
        temp_row = mynext()
        header_info['y_axis_units'] = temp_row[1]
        temp_row = mynext()

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
        elif num_traces == 6:
            for row in data:
                data_array.append((float(row[0]),
                                   [float(row[1]),
                                   float(row[2]),
                                   float(row[3]),
                                   float(row[4]),
                                   float(row[5]),
                                   float(row[6])]))
            data = np.array(
                data_array,
                dtype={'names': ('frequency', 'amplitude'),
                       'formats': ('f8', '6f8')})
    return (header_info, data)


def _get_ref(s):
    """Convert given string into the reference level
    """
    match = re.search(r'[\d.]+', s)
    if match:
        return float(match.group())
    else:
        return ''
