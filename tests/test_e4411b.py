# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Unit tests for keysight/e4411b.py.
"""
# Try to future proof code so that it's Python 3.x ready
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import unittest
import logging

from unipath import Path

from keysight import e4411b

TEST_DIR = Path(__file__).ancestor(1)

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format=' %(asctime)s -  %(levelname)s - %(message)s'
)


class TestReadingCSVFiles(unittest.TestCase):

    def setUp(self):
        test_csv_file = Path(TEST_DIR, 'sample_data', 'E4411DATA.CSV')
        print(test_csv_file)
        (self.header, self.data) = e4411b.read_csv_file(
            test_csv_file)

    def test_header_when_reading_csv_file(self):
        self.assertEqual(self.header['timestamp'],
                         ' 07/29/15   12:12:29')
        self.assertEqual(self.header['file'],
                         'A:\\TRACE080.CSV')
        self.assertEqual(self.header['title'], '')
        self.assertEqual(self.header['model'], 'E4411B')
        self.assertEqual(self.header['serial_number'], 'MY45104634')
        self.assertEqual(self.header['center_freq'], 750000000.0)
        self.assertEqual(self.header['span_freq'], 500000000.0)
        self.assertEqual(self.header['resolution_bw'], 100000)
        self.assertEqual(self.header['video_bw'], 100000)
        self.assertEqual(self.header['sweep_time'], 0.0644205)
        self.assertEqual(self.header['num_traces'], 3)
        self.assertEqual(self.header['num_points'], 401)

    def test_data_when_reading_csv_file(self):
        self.assertEqual(self.data.shape, (401,))
        self.assertEqual(self.data['amplitude'].shape, (401, 3))
        self.assertEqual(self.data['frequency'][0], 500000000)
        self.assertEqual(self.data['amplitude'][0][0], 3.7123)
        self.assertEqual(self.data['amplitude'][0][1], -2147.48)
        self.assertEqual(self.data['amplitude'][0][2], -2147.48)
        self.assertEqual(self.data['frequency'][1], 501250000)
        self.assertEqual(self.data['amplitude'][1][0], 3.3353)
        self.assertEqual(self.data['frequency'][-2], 998750000)
        self.assertEqual(self.data['amplitude'][-2][0], 3.9023)
        self.assertEqual(self.data['frequency'][-1], 1000000000)
        self.assertEqual(self.data['amplitude'][-1][0], 3.5163)

if __name__ == '__main__':
    unittest.main()
