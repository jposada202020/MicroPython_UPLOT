# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`utils`
================================================================================

Plot Utilities


* Author: Jose D. Montoya


"""


# Taken from
# https://stackoverflow.com/questions/12334442/does-python-have-a-linspace-function-in-its-std-lib


def linspace(start, stop, n):
    """
    Creates a linearspace
    """
    if n == 1:
        yield stop
        return
    delta = (stop - start) / (n - 1)
    for i in range(n):
        yield start + delta * i
