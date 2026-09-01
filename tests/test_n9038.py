# Copyright (c) 2013-2026 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Unit tests for keysight/n9038.py."""

import numpy as np
import pytest

from keysight import n9038

# The two files are the same sweep saved both ways: AllTraces carries all six
# traces, Trace carries only the one, and the reader shapes the amplitude
# field differently for each.
COMMON_HEADER = {
    "instrument_ver": "A.25.08",
    "model_num": "N9038A",
    "num_points": 1001,
    "start_freq": 30000000,
    "stop_freq": 300000000,
    "average_count": 0,
    "rbw_filter": "Gaussian",
    "sweep_type": "Swept",
    "x_axis_scale": "Lin",
    "preamp_state": "Off",
    "preamp_band": "Low",
    "trigger_source": "Free",
    "trigger_level": 1.2,
    "trigger_slope": "Positive",
    "trigger_delay": 0,
    "phase_noise_optimization": "Fast",
    "swept_if_gain": "Low",
    "fft_if_gain": "Autorange",
    "rf_coupling": "DC",
    "fft_width": 411900,
    "ext_ref": 10000000,
    "input": "RF",
    "rf_calibration": "Off",
    "attenuation": 6,
    "ref_level_offset": 0,
    "external_gain": 0,
    "trace_type": "Maxhold",
    "detector": "Peak",
    "trace_math_offset": 0,
    "normalize": "Off",
    "x_axis_units": "Hz",
    "y_axis_units": "dBuV",
}

ALL_TRACES_HEADER = COMMON_HEADER | {
    "data_file_type": "AllTrace",
    "sweep_time": 0.030133333333,
    "average_type": "Voltage",
    "rbw": 120000,
    "rbw_filter_bw": "6dB",
    "vbw": 91000,
    "num_traces": 6,
    "trace_math": ["Off"] * 6,
    "trace_math_oper1": ["Trace5", "Trace6", "Trace1", "Trace2", "Trace3", "Trace4"],
    "trace_math_oper2": ["Trace6", "Trace1", "Trace2", "Trace3", "Trace4", "Trace5"],
    "trace_name": ["Trace1", "Trace2", "Trace3", "Trace4", "Trace5", "Trace6"],
}

ONE_TRACE_HEADER = COMMON_HEADER | {
    "data_file_type": "Trace",
    "sweep_time": 2.492066666667,
    "average_type": "LogPower(Video)",
    "rbw": 10000,
    "rbw_filter_bw": "3dB",
    "vbw": 10000,
    "num_traces": 1,
    "trace_math": ["Off"],
    "trace_math_oper1": ["Trace5"],
    "trace_math_oper2": ["Trace6"],
    "trace_name": ["Trace1"],
}


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("N9038A_AllTraces.csv", ALL_TRACES_HEADER),
        ("N9038A_OneTrace.csv", ONE_TRACE_HEADER),
    ],
)
def test_header_when_reading_n9038_file(sample_data, filename, expected):
    header, _ = n9038.read_csv_file(sample_data(filename))
    assert header == expected


# The first two and last two rows of each file, which is what pins down the
# frequency axis and the amplitude column ordering at both ends of the sweep.
EDGE_ROWS = [0, 1, -2, -1]
EDGE_FREQUENCIES = [30000000, 30270000, 299730000, 300000000]


def test_data_when_reading_all_traces_file(sample_data):
    _, data = n9038.read_csv_file(sample_data("N9038A_AllTraces.csv"))
    assert data.shape == (1001,)
    assert data["amplitude"].shape == (1001, 6)
    np.testing.assert_array_equal(data["frequency"][EDGE_ROWS], EDGE_FREQUENCIES)
    np.testing.assert_array_equal(
        data["amplitude"][EDGE_ROWS, 0],
        [
            15.9102265632965,
            18.8954552564408,
            15.9155117211024,
            16.4202117491917,
        ],
    )
    # The second trace, so that a reader collapsing the traces into one column
    # would not pass on the first alone.
    np.testing.assert_array_equal(data["amplitude"][0, 1], 12.5327250075504)


def test_data_when_reading_one_trace_file(sample_data):
    _, data = n9038.read_csv_file(sample_data("N9038A_OneTrace.csv"))
    assert data.shape == (1001,)
    # Scalar rather than a length one sequence.
    assert data["amplitude"].shape == (1001,)
    np.testing.assert_array_equal(data["frequency"][EDGE_ROWS], EDGE_FREQUENCIES)
    np.testing.assert_array_equal(
        data["amplitude"][EDGE_ROWS],
        [
            12.7683034120476,
            8.69782545038416,
            10.1010586765782,
            8.31183394722589,
        ],
    )
