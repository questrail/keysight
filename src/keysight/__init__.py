# Copyright (c) 2013-2026 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Read data files saved by Keysight/Agilent/HP test equipment.

Each supported instrument gets a module of its own, since every one of them
writes a different header, and each module exposes `read_csv_file()`. The
modules are imported here so that `import keysight` is enough to reach any of
them, rather than each caller having to know the submodule import form.
"""

from . import e4411b, n9038, n9340

__all__ = [
    "e4411b",
    "n9038",
    "n9340",
]
