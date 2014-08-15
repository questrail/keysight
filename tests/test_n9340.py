# -*- coding: utf-8 -*-
# Copyright (c) 2013 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Unit tests for keysight/n9340.py.
"""
# Try to future proof code so that it's Python 3.x ready
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import unittest

from unipath import Path

TEST_DIR = Path(__file__).ancestor(1)

from keysight import n9340


class TestReadingCSVFiles(unittest.TestCase):

    def setUp(self):
        test_csv_file = Path(TEST_DIR, 'sample_data', 'RET1AMB.CSV')
        (self.n9340_header, self.n9340_data) = n9340.read_csv_file(
            test_csv_file)

    def test_reading_n9340_file(self):
        self.assertEual(self.n9340_header['file'],
                        '/bd0/N9340DATA/RET1AMB.CSV')

if __name__ == '__main__':
    unittest.main()
