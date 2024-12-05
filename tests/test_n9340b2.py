# -*- coding: utf-8 -*-
# Copyright (c) 2013-2024 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Unit tests for keysight/n9340.py."""

import unittest

from unipath import Path

from keysight import n9340

TEST_DIR = Path(__file__).ancestor(1)


class TestReadingCSVFiles(unittest.TestCase):
    def setUp(self):
        test_csv_file = Path(TEST_DIR, "sample_data", "N9340B2.CSV")
        (self.n9340_header, self.n9340_data) = n9340.read_csv_file(test_csv_file)

    def test_header_when_reading_n9340_file(self):
        self.assertEqual(self.n9340_header["file"], "/bd0/N9340DATA/CHAMBBH.CSV")
        self.assertEqual(self.n9340_header["system_parameter"], "Default Unit:dBm/Hz/s")
        self.assertEqual(self.n9340_header["ref"], 106.0)
        self.assertEqual(self.n9340_header["ref_offset"], 0.0)
        self.assertEqual(self.n9340_header["start_freq"], 30e6)
        self.assertEqual(self.n9340_header["stop_freq"], 300e6)
        self.assertEqual(self.n9340_header["center_freq"], 165000000)
        self.assertEqual(self.n9340_header["span_freq"], 270000000)
        self.assertEqual(self.n9340_header["vbw"], 100000)
        self.assertEqual(self.n9340_header["vbw_mode"], "AUTO")
        self.assertEqual(self.n9340_header["rbw"], 100000)
        self.assertEqual(self.n9340_header["rbw_mode"], "MAN")
        self.assertEqual(self.n9340_header["vbw_to_rbw"], 1)
        self.assertEqual(self.n9340_header["vbw_to_rbw_mode"], "AUTO")
        self.assertEqual(self.n9340_header["sweep_time"], 1.225115)
        self.assertEqual(self.n9340_header["sweep_time_mode"], "AUTO")
        self.assertEqual(self.n9340_header["attenuation"], 20)
        self.assertEqual(self.n9340_header["attenuation_mode"], "AUTO")
        self.assertEqual(self.n9340_header["scale_div"], 10)
        self.assertEqual(self.n9340_header["scale_type"], "LOG")
        self.assertEqual(self.n9340_header["preamp"], "OFF")
        self.assertEqual(self.n9340_header["psd_mode"], "OFF")
        self.assertEqual(self.n9340_header["trace_unit"], "dBuV")

    def test_data_when_reading_n9340_file(self):
        self.assertEqual(self.n9340_data.shape, (461,))
        self.assertEqual(self.n9340_data["frequency"][0], 30e6)
        self.assertEqual(self.n9340_data["amplitude_db"][0], 43.19)
        self.assertEqual(self.n9340_data["frequency"][1], 30586956.521739)
        self.assertEqual(self.n9340_data["amplitude_db"][1], 44.14)


if __name__ == "__main__":
    unittest.main()
