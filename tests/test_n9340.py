# Copyright (c) 2013-2026 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Unit tests for keysight/n9340.py."""

import pytest

from keysight import n9340

# The three files differ in the ways the reader has to cope with: RET1AMB
# writes a bare reference level, N9340B appends units to it, N9340B2 appends
# units and carries a marker block ahead of the trace data, and TST is a full
# span sweep that starts at 0 Hz.
RET1AMB_HEADER = {
    "file": "/bd0/N9340DATA/RET1AMB.CSV",
    "system_parameter": "Default Unit:dBm/Hz/s",
    "ref": 0.0,
    "ref_offset": 0.0,
    "start_freq": 100000,
    "stop_freq": 30000000,
    "center_freq": 15050000,
    "span_freq": 29900000,
    "vbw": 10000,
    "vbw_mode": "AUTO",
    "rbw": 10000,
    "rbw_mode": "MAN",
    "vbw_to_rbw": 1,
    "vbw_to_rbw_mode": "AUTO",
    "sweep_time": 1.278503,
    "sweep_time_mode": "AUTO",
    "attenuation": 20,
    "attenuation_mode": "AUTO",
    "scale_div": 10,
    "scale_type": "LOG",
    "preamp": "OFF",
    "psd_mode": "OFF",
    "trace_unit": "dBm",
}

N9340B_HEADER = RET1AMB_HEADER | {"file": "/bd0/N9340DATA/A10.CSV"}

N9340B2_HEADER = RET1AMB_HEADER | {
    "file": "/bd0/N9340DATA/CHAMBBH.CSV",
    "ref": 106.0,
    "start_freq": 30e6,
    "stop_freq": 300e6,
    "center_freq": 165000000,
    "span_freq": 270000000,
    "vbw": 100000,
    "rbw": 100000,
    "sweep_time": 1.225115,
    "trace_unit": "dBuV",
}

TST_HEADER = RET1AMB_HEADER | {
    "file": "/bd0/N9340DATA/TST.CSV",
    "start_freq": 0,
    "stop_freq": 3e9,
    "center_freq": 1.5e9,
    "span_freq": 3e9,
    "vbw": 1e6,
    "rbw": 1e6,
    "rbw_mode": "AUTO",
    "sweep_time": 1.074067,
}


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("RET1AMB.CSV", RET1AMB_HEADER),
        ("N9340B.CSV", N9340B_HEADER),
        ("N9340B2.CSV", N9340B2_HEADER),
        ("N9340B Test Files/TST.CSV", TST_HEADER),
    ],
)
def test_header_when_reading_n9340_file(sample_data, filename, expected):
    header, _ = n9340.read_csv_file(sample_data(filename))
    assert {key: header[key] for key in expected} == expected


@pytest.mark.parametrize(
    ("filename", "expected_rows"),
    [
        (
            "RET1AMB.CSV",
            [
                (0, 100000, -47.25),
                (1, 165000, -47.11),
                (-2, 29935000, -75.66),
                (-1, 30000000, -74.7),
            ],
        ),
        (
            "N9340B.CSV",
            [
                (0, 100000, -43.73),
                (1, 165000, -52.12),
                (-2, 29935000, -72.84),
                (-1, 30000000, -73.79),
            ],
        ),
        (
            "N9340B2.CSV",
            [
                (0, 30e6, 43.19),
                (1, 30586956.521739, 44.14),
            ],
        ),
        (
            "N9340B Test Files/TST.CSV",
            [
                (0, 0.0, 3.54),
                (1, 6521739.130435, -56.85),
            ],
        ),
    ],
)
def test_data_when_reading_n9340_file(sample_data, filename, expected_rows):
    _, data = n9340.read_csv_file(sample_data(filename))
    assert data.shape == (461,)
    for index, frequency, amplitude in expected_rows:
        assert data["frequency"][index] == frequency
        assert data["amplitude_db"][index] == amplitude


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("0.00", 0.0),
        ("106.00dBuV", 106.0),
        (" 0.00dBm ", 0.0),
        # A reference level with no digits in it at all, which the reader
        # reports as an empty string rather than guessing a level.
        ("", ""),
        ("N/A", ""),
    ],
)
def test_get_ref_reads_the_level_with_or_without_units(field, expected):
    assert n9340._get_ref(field) == expected
