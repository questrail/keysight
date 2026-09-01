# Copyright (c) 2013-2026 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Unit tests for keysight/_tracedata.py."""

import pytest

from keysight._tracedata import read_trace_rows


def test_columns_past_the_traces_are_ignored():
    # These instruments are prone to a trailing empty field on a data row,
    # and a reader that passed the whole row through would try to float() it.
    data = read_trace_rows([["1e6", "-10.0", ""], ["2e6", "-11.0", ""]], 1)
    assert data["frequency"].tolist() == [1e6, 2e6]
    assert data["amplitude"].tolist() == [-10.0, -11.0]


def test_a_trace_count_below_one_is_refused():
    with pytest.raises(ValueError, match="at least one trace"):
        read_trace_rows([["1e6"]], 0)
