# Copyright (c) 2013-2026 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Read a CSV file saved by an E4411B Spectrum Analyzer"""

# Standard module imports
import csv
from os import PathLike
from typing import Any

# Data analysis related imports
import numpy.typing as npt

from ._tracedata import read_trace_rows


def read_csv_file(
    filename: str | PathLike[str],
) -> tuple[dict[str, Any], npt.NDArray]:
    """Read csv file into a numpy array

    Args:
        filename: Path to a CSV file saved by an E4411B or E4402B spectrum
            analyzer.

    Returns:
        A tuple containing:
            A dict of the header fields read from the top of the file.
            A 1D numpy structured array with the fields 'frequency' and
                'amplitude'. The 'amplitude' field is scalar for a single
                trace file and holds one value per trace otherwise.

    Raises:
        ValueError: If the trace header row names no traces at all.
    """
    header_info: dict[str, Any] = {}

    with open(filename, newline="", encoding="utf8") as csvfile:
        # The analyzer pads its files with NUL bytes, which csv.reader treats
        # as an error rather than as whitespace, so strip them per line before
        # the reader ever sees them.
        data = csv.reader((line.replace("\0", "") for line in csvfile), delimiter=",")
        mynext = data.__next__
        temp_row = mynext()
        header_info["timestamp"] = temp_row[0]
        header_info["file"] = temp_row[1]
        header_info["title"] = mynext()[1]
        header_info["model"] = mynext()[1]
        header_info["serial_number"] = mynext()[1]
        header_info["center_freq"] = float(mynext()[1])
        header_info["span_freq"] = float(mynext()[1])
        header_info["resolution_bw"] = float(mynext()[1])
        header_info["video_bw"] = float(mynext()[1])
        header_info["ref_level"] = float(mynext()[1])
        header_info["sweep_time"] = float(mynext()[1])
        header_info["num_points"] = int(mynext()[1])
        mynext()  # Skip blank line 12
        mynext()  # Skip blank line 13
        # The trace header names one column per trace after the frequency
        # column, so its width is what says how many traces the file holds.
        num_traces = len(mynext()) - 1
        header_info["num_traces"] = num_traces
        header_info["frequency"] = mynext()[0]

        data_array = read_trace_rows(data, num_traces)

    return (header_info, data_array)
