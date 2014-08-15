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
import os.path

# Data analysis related imports
import numpy as np


def read_csv_file(filename):
    """Read csv file into a numpy array
    """
    # FIXME: Test a file with blank lines in the CSV file.
    header_data = {}
    with open(filename, 'rb') as csvfile:
        data = csv.reader((line.replace(b'\0', b'') for line in csvfile),
                          delimiter=b',')
        header_data['file'] = data.next()[1]

    print(header_data['file'])
