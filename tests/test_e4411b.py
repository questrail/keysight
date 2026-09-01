# Copyright (c) 2013-2026 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Unit tests for keysight/e4411b.py."""

import numpy as np
import pytest

from keysight import e4411b

# Where the trace columns start in an E4411B file. Everything above it is
# one header field per line, and some of those lines carry a units column that
# must survive the trimming below.
FIRST_TRACE_ROW = 13


@pytest.fixture
def three_trace_file(sample_data):
    return sample_data("E4411DATA.CSV")


@pytest.fixture
def fewer_traces(three_trace_file, tmp_path):
    """Return a callable making a copy of the sample file with N traces.

    The only E4411B file to hand holds three traces, and the reader treats a
    single trace file differently from a multi trace one, so the other shapes
    are cut from the file that does exist rather than left unexercised.
    """

    def trim(num_traces: int):
        lines = three_trace_file.read_text(encoding="utf8").splitlines()
        trimmed = [
            ",".join(line.split(",")[: num_traces + 1])
            if index >= FIRST_TRACE_ROW
            else line
            for index, line in enumerate(lines)
        ]
        path = tmp_path / f"E4411_{num_traces}trace.CSV"
        path.write_text("\n".join(trimmed), encoding="utf8")
        return path

    return trim


def test_header_when_reading_csv_file(three_trace_file):
    header, _ = e4411b.read_csv_file(three_trace_file)
    assert header == {
        "timestamp": " 07/29/15   12:12:29",
        "file": "A:\\TRACE080.CSV",
        "title": "",
        "model": "E4411B",
        "serial_number": "MY45104634",
        "center_freq": 750000000.0,
        "span_freq": 500000000.0,
        "resolution_bw": 100000,
        "video_bw": 100000,
        "ref_level": 73.0103,
        "sweep_time": 0.0644205,
        "num_points": 401,
        "num_traces": 3,
        "frequency": "Hz",
    }


# The first two and last two rows, which is what pins down the frequency axis
# and the amplitude column ordering at both ends of the sweep.
EDGE_ROWS = [0, 1, -2, -1]
EDGE_FREQUENCIES = [500000000, 501250000, 998750000, 1000000000]
EDGE_TRACE1 = [3.7123, 3.3353, 3.9023, 3.5163]


def test_data_when_reading_csv_file(three_trace_file):
    _, data = e4411b.read_csv_file(three_trace_file)
    assert data.shape == (401,)
    assert data["amplitude"].shape == (401, 3)
    np.testing.assert_array_equal(data["frequency"][EDGE_ROWS], EDGE_FREQUENCIES)
    np.testing.assert_array_equal(data["amplitude"][EDGE_ROWS, 0], EDGE_TRACE1)
    # Traces 2 and 3 were off for this sweep, so they sit at the analyzer's
    # floor value. They are checked so that a reader collapsing the traces
    # into one column would not pass on trace 1 alone.
    np.testing.assert_array_equal(
        data["amplitude"][[0, 1], 1:],
        [[-2147.48, -2147.48], [-2147.48, -2147.48]],
    )


@pytest.mark.parametrize("num_traces", [1, 2])
def test_the_amplitude_field_follows_the_trace_count(fewer_traces, num_traces):
    header, data = e4411b.read_csv_file(fewer_traces(num_traces))
    assert header["num_traces"] == num_traces
    if num_traces == 1:
        # Scalar rather than a length one sequence, so that a one trace file
        # reads as data['amplitude'][i] the way the N9340 reader's output does.
        assert data["amplitude"].shape == (401,)
        trace1 = data["amplitude"][EDGE_ROWS]
    else:
        assert data["amplitude"].shape == (401, num_traces)
        trace1 = data["amplitude"][EDGE_ROWS, 0]
    np.testing.assert_array_equal(data["frequency"][EDGE_ROWS], EDGE_FREQUENCIES)
    np.testing.assert_array_equal(trace1, EDGE_TRACE1)


def test_a_file_naming_no_traces_is_refused(fewer_traces):
    # Trimming to zero traces leaves the trace header row as a lone label,
    # which used to return the spent CSV reader in place of an array.
    with pytest.raises(ValueError, match="at least one trace"):
        e4411b.read_csv_file(fewer_traces(0))
