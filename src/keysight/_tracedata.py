# Copyright (c) 2013-2026 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Build a trace array from the data rows of an instrument CSV file.

The E4411B and the N9038 write different headers and then the same thing
underneath them: rows of a frequency followed by one amplitude per trace. The
trace count varies per file rather than per instrument, so the array
construction lives here instead of being spelled out once per trace count in
each module. The N9340 is not a caller: it is always single trace and names
its amplitude field 'amplitude_db', which callers index by name.
"""

from collections.abc import Iterable
from typing import Any

import numpy as np
import numpy.typing as npt


def read_trace_rows(rows: Iterable[list[str]], num_traces: int) -> npt.NDArray:
    """Read frequency/amplitude rows into a numpy structured array.

    Args:
        rows: The data rows of an instrument CSV file, each holding a
            frequency followed by one amplitude per trace. Any columns past
            the traces are ignored, since these instruments are prone to
            writing a trailing empty field.
        num_traces: How many amplitude columns follow the frequency column.

    Returns:
        A 1D numpy structured array with the fields 'frequency' and
        'amplitude'. The 'amplitude' field is scalar when there is a single
        trace, so that a one trace file indexes as data['amplitude'][i] rather
        than as a length one sequence.

    Raises:
        ValueError: If num_traces is not at least one.
    """
    if num_traces < 1:
        raise ValueError(f"Expected at least one trace, got {num_traces}")

    data_rows: list[tuple[float, Any]] = []
    for row in rows:
        amplitudes = [float(value) for value in row[1 : num_traces + 1]]
        data_rows.append(
            (float(row[0]), amplitudes[0] if num_traces == 1 else amplitudes)
        )

    return np.array(
        data_rows,
        dtype={
            "names": ("frequency", "amplitude"),
            "formats": ("f8", "f8" if num_traces == 1 else f"{num_traces}f8"),
        },
    )
