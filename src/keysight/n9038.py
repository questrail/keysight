# Copyright (c) 2013-2026 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Read a CSV file saved by an N9038 EMI Test Receiver"""

# Standard module imports
import csv
from collections.abc import Callable
from os import PathLike
from typing import Any

# Data analysis related imports
import numpy.typing as npt

from ._tracedata import read_trace_rows

# Most of an N9038 header is one field per line, written as a label followed
# by a single value. Those lines are listed here in file order, with the
# conversion each value needs, rather than spelled out one assignment at a
# time: the reader then walks the table, and adding a field the receiver
# started writing is a line here instead of a line in the middle of the parse.
_SINGLE_VALUE_FIELDS: tuple[tuple[str, Callable[[str], Any]], ...] = (
    ("num_points", float),
    ("sweep_time", float),
    ("start_freq", float),
    ("stop_freq", float),
    ("average_count", float),
    ("average_type", str),
    ("rbw", float),
    ("rbw_filter", str),
    ("rbw_filter_bw", str),
    ("vbw", float),
    ("sweep_type", str),
    ("x_axis_scale", str),
    ("preamp_state", str),
    ("preamp_band", str),
    ("trigger_source", str),
    ("trigger_level", float),
    ("trigger_slope", str),
    ("trigger_delay", float),
    ("phase_noise_optimization", str),
    ("swept_if_gain", str),
    ("fft_if_gain", str),
    ("rf_coupling", str),
    ("fft_width", float),
    ("ext_ref", float),
    ("input", str),
    ("rf_calibration", str),
    ("attenuation", float),
    ("ref_level_offset", float),
    ("external_gain", float),
    ("trace_type", str),
    ("detector", str),
)

# The three lines after the single value block hold one value per trace rather
# than one value, so they are read together and kept as lists.
_PER_TRACE_FIELDS: tuple[str, ...] = (
    "trace_math",
    "trace_math_oper1",
    "trace_math_oper2",
)


def read_csv_file(
    filename: str | PathLike[str],
) -> tuple[dict[str, Any], npt.NDArray]:
    """Read csv file into a numpy array

    Args:
        filename: Path to a CSV file saved by an N9038 EMI test receiver.

    Returns:
        A tuple containing:
            A dict of the header fields read from the top of the file.
            A 1D numpy structured array with the fields 'frequency' and
                'amplitude'. The 'amplitude' field is scalar for a single
                trace file and holds one value per trace otherwise.

    Raises:
        ValueError: If the trace name row names no traces at all.
    """
    header_info: dict[str, Any] = {}

    with open(filename, newline="", encoding="utf8") as csvfile:
        # The receiver pads its files with NUL bytes, which csv.reader treats
        # as an error rather than as whitespace, so strip them per line before
        # the reader ever sees them.
        data = csv.reader((line.replace("\0", "") for line in csvfile), delimiter=",")
        mynext = data.__next__

        header_info["data_file_type"] = mynext()[0]
        mynext()  # Skip the blank line under the file type
        temp_row = mynext()
        header_info["instrument_ver"] = temp_row[0]
        header_info["model_num"] = temp_row[1]
        mynext()  # Skip the two lines between the model and the settings
        mynext()

        for key, convert in _SINGLE_VALUE_FIELDS:
            header_info[key] = convert(mynext()[1])

        for key in _PER_TRACE_FIELDS:
            header_info[key] = mynext()[1:]

        header_info["trace_math_offset"] = float(mynext()[1])
        header_info["normalize"] = mynext()[1]

        # The trace name row names one trace per column after the label, so
        # its width is what says how many traces the file holds.
        temp_row = mynext()
        num_traces = len(temp_row) - 1
        header_info["num_traces"] = num_traces
        header_info["trace_name"] = temp_row[1:]

        header_info["x_axis_units"] = mynext()[1]
        header_info["y_axis_units"] = mynext()[1]
        mynext()  # Skip the DATA marker that precedes the rows

        data_array = read_trace_rows(data, num_traces)

    return (header_info, data_array)
