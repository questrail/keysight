# -*- coding: utf-8 -*-
# Copyright (c) 2013-2023 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Unit tests for keysight/n9038.py.
"""

import unittest

from unipath import Path

from keysight import n9038

TEST_DIR = Path(__file__).ancestor(1)


class TestReadingCSVFileAllTraces(unittest.TestCase):
    def setUp(self):
        test_csv_file = Path(TEST_DIR, "sample_data", "N9038A_AllTraces.CSV")
        print(test_csv_file)
        (self.header, self.data) = n9038.read_csv_file(test_csv_file)

    def test_header_when_reading_n9038_file(self):
        self.assertEqual(self.header["data_file_type"], "AllTrace")
        self.assertEqual(self.header["instrument_ver"], "A.25.08")
        self.assertEqual(self.header["model_num"], "N9038A")
        self.assertEqual(self.header["num_points"], 1001)
        self.assertEqual(self.header["sweep_time"], 0.030133333333)
        self.assertEqual(self.header["start_freq"], 30000000)
        self.assertEqual(self.header["stop_freq"], 300000000)
        self.assertEqual(self.header["average_count"], 0)
        self.assertEqual(self.header["average_type"], "Voltage")
        self.assertEqual(self.header["rbw"], 120000)
        self.assertEqual(self.header["rbw_filter"], "Gaussian")
        self.assertEqual(self.header["rbw_filter_bw"], "6dB")
        self.assertEqual(self.header["vbw"], 91000)
        self.assertEqual(self.header["sweep_type"], "Swept")
        self.assertEqual(self.header["x_axis_scale"], "Lin")
        self.assertEqual(self.header["preamp_state"], "Off")
        self.assertEqual(self.header["preamp_band"], "Low")
        self.assertEqual(self.header["trigger_source"], "Free")
        self.assertEqual(self.header["trigger_level"], 1.2)
        self.assertEqual(self.header["trigger_slope"], "Positive")
        self.assertEqual(self.header["trigger_delay"], 0)
        self.assertEqual(self.header["phase_noise_optimization"], "Fast")
        self.assertEqual(self.header["swept_if_gain"], "Low")
        self.assertEqual(self.header["fft_if_gain"], "Autorange")
        self.assertEqual(self.header["rf_coupling"], "DC")
        self.assertEqual(self.header["fft_width"], 411900)
        self.assertEqual(self.header["ext_ref"], 10000000)
        self.assertEqual(self.header["input"], "RF")
        self.assertEqual(self.header["rf_calibration"], "Off")
        self.assertEqual(self.header["attenuation"], 6)
        self.assertEqual(self.header["ref_level_offset"], 0)
        self.assertEqual(self.header["external_gain"], 0)
        self.assertEqual(self.header["trace_type"], "Maxhold")
        self.assertEqual(self.header["detector"], "Peak")
        self.assertEqual(self.header["trace_math"][0], "Off")
        self.assertEqual(self.header["trace_math"][1], "Off")
        self.assertEqual(self.header["trace_math"][2], "Off")
        self.assertEqual(self.header["trace_math"][3], "Off")
        self.assertEqual(self.header["trace_math"][4], "Off")
        self.assertEqual(self.header["trace_math"][5], "Off")
        self.assertEqual(self.header["trace_math_oper1"][0], "Trace5")
        self.assertEqual(self.header["trace_math_oper1"][1], "Trace6")
        self.assertEqual(self.header["trace_math_oper1"][2], "Trace1")
        self.assertEqual(self.header["trace_math_oper1"][3], "Trace2")
        self.assertEqual(self.header["trace_math_oper1"][4], "Trace3")
        self.assertEqual(self.header["trace_math_oper1"][5], "Trace4")
        self.assertEqual(self.header["trace_math_oper2"][0], "Trace6")
        self.assertEqual(self.header["trace_math_oper2"][1], "Trace1")
        self.assertEqual(self.header["trace_math_oper2"][2], "Trace2")
        self.assertEqual(self.header["trace_math_oper2"][3], "Trace3")
        self.assertEqual(self.header["trace_math_oper2"][4], "Trace4")
        self.assertEqual(self.header["trace_math_oper2"][5], "Trace5")
        self.assertEqual(self.header["trace_math_offset"], 0)
        self.assertEqual(self.header["normalize"], "Off")
        self.assertEqual(self.header["trace_name"][0], "Trace1")
        self.assertEqual(self.header["trace_name"][1], "Trace2")
        self.assertEqual(self.header["trace_name"][2], "Trace3")
        self.assertEqual(self.header["trace_name"][3], "Trace4")
        self.assertEqual(self.header["trace_name"][4], "Trace5")
        self.assertEqual(self.header["trace_name"][5], "Trace6")
        self.assertEqual(self.header["x_axis_units"], "Hz")
        self.assertEqual(self.header["y_axis_units"], "dBuV")

    def test_data_when_reading_n9038_file(self):
        self.assertEqual(self.data.shape, (1001,))
        self.assertEqual(self.data["amplitude"].shape, (1001, 6))
        self.assertEqual(self.data["frequency"][0], 30000000)
        self.assertEqual(self.data["amplitude"][0][0], 15.9102265632965)
        self.assertEqual(self.data["amplitude"][0][1], 12.5327250075504)
        self.assertEqual(self.data["frequency"][1], 30270000)
        self.assertEqual(self.data["amplitude"][1][0], 18.8954552564408)
        self.assertEqual(self.data["frequency"][-1], 300000000)
        self.assertEqual(self.data["amplitude"][-1][0], 16.4202117491917)
        self.assertEqual(self.data["frequency"][-2], 299730000)
        self.assertEqual(self.data["amplitude"][-2][0], 15.9155117211024)


class TestReadingCSVFileOneTrace(unittest.TestCase):
    def setUp(self):
        test_csv_file = Path(TEST_DIR, "sample_data", "N9038A_OneTrace.CSV")
        print(test_csv_file)
        (self.header, self.data) = n9038.read_csv_file(test_csv_file)

    def test_header_when_reading_n9038_file(self):
        self.assertEqual(self.header["data_file_type"], "Trace")
        self.assertEqual(self.header["instrument_ver"], "A.25.08")
        self.assertEqual(self.header["model_num"], "N9038A")
        self.assertEqual(self.header["num_points"], 1001)
        self.assertEqual(self.header["sweep_time"], 2.492066666667)
        self.assertEqual(self.header["start_freq"], 30000000)
        self.assertEqual(self.header["stop_freq"], 300000000)
        self.assertEqual(self.header["average_count"], 0)
        self.assertEqual(self.header["average_type"], "LogPower(Video)")
        self.assertEqual(self.header["rbw"], 10000)
        self.assertEqual(self.header["rbw_filter"], "Gaussian")
        self.assertEqual(self.header["rbw_filter_bw"], "3dB")
        self.assertEqual(self.header["vbw"], 10000)
        self.assertEqual(self.header["sweep_type"], "Swept")
        self.assertEqual(self.header["x_axis_scale"], "Lin")
        self.assertEqual(self.header["preamp_state"], "Off")
        self.assertEqual(self.header["preamp_band"], "Low")
        self.assertEqual(self.header["trigger_source"], "Free")
        self.assertEqual(self.header["trigger_level"], 1.2)
        self.assertEqual(self.header["trigger_slope"], "Positive")
        self.assertEqual(self.header["trigger_delay"], 0)
        self.assertEqual(self.header["phase_noise_optimization"], "Fast")
        self.assertEqual(self.header["swept_if_gain"], "Low")
        self.assertEqual(self.header["fft_if_gain"], "Autorange")
        self.assertEqual(self.header["rf_coupling"], "DC")
        self.assertEqual(self.header["fft_width"], 411900)
        self.assertEqual(self.header["ext_ref"], 10000000)
        self.assertEqual(self.header["input"], "RF")
        self.assertEqual(self.header["rf_calibration"], "Off")
        self.assertEqual(self.header["attenuation"], 6)
        self.assertEqual(self.header["ref_level_offset"], 0)
        self.assertEqual(self.header["external_gain"], 0)
        self.assertEqual(self.header["trace_type"], "Maxhold")
        self.assertEqual(self.header["detector"], "Peak")
        self.assertEqual(self.header["trace_math"][0], "Off")
        self.assertEqual(self.header["trace_math_oper1"][0], "Trace5")
        self.assertEqual(self.header["trace_math_oper2"][0], "Trace6")
        self.assertEqual(self.header["trace_math_offset"], 0)
        self.assertEqual(self.header["normalize"], "Off")
        self.assertEqual(self.header["trace_name"][0], "Trace1")
        self.assertEqual(self.header["x_axis_units"], "Hz")
        self.assertEqual(self.header["y_axis_units"], "dBuV")

    def test_data_when_reading_n9038_file(self):
        self.assertEqual(self.data.shape, (1001,))
        self.assertEqual(self.data["amplitude"].shape, (1001, 1))
        self.assertEqual(self.data["frequency"][0], 30000000)
        self.assertEqual(self.data["amplitude"][0], 12.7683034120476)
        self.assertEqual(self.data["frequency"][1], 30270000)
        self.assertEqual(self.data["amplitude"][1], 8.69782545038416)
        self.assertEqual(self.data["frequency"][-1], 300000000)
        self.assertEqual(self.data["amplitude"][-1], 8.31183394722589)
        self.assertEqual(self.data["frequency"][-2], 299730000)
        self.assertEqual(self.data["amplitude"][-2], 10.1010586765782)


if __name__ == "__main__":
    unittest.main()
