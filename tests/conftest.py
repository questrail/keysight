# Copyright (c) 2013-2026 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Fixtures shared by the keysight unit tests."""

import pathlib

import pytest

SAMPLE_DATA_DIR = pathlib.Path(__file__).parent / "sample_data"


@pytest.fixture
def sample_data():
    """Return a callable that resolves a name under tests/sample_data."""

    def resolve(name: str) -> pathlib.Path:
        path = SAMPLE_DATA_DIR / name
        if not path.is_file():
            # Without this, a renamed or missing sample file surfaces as
            # whatever the reader happens to raise on a path that isn't there,
            # which reads as a parsing failure rather than a missing fixture.
            raise FileNotFoundError(f"No sample data file named {name}")
        return path

    return resolve
