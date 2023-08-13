# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`colors`
================================================================================

MicroPython Graphics Library


* Author: Jose D. Montoya


"""


def create_color(ssd, idx, r, g, b):
    """
    Creates a color in the LUT of the display and returns the index."""

    color = ssd.rgb(r, g, b)

    x = idx << 1
    ssd.lut[x] = color & 0xFF
    ssd.lut[x + 1] = color >> 8
    return idx


def set_color(display, idx, r, g, b):
    """
    Sets the color in the LUT of the display and returns the index.
    """
    if hasattr(display, "lut"):
        return create_color(display, idx, r, g, b)
    return display.rgb(r, g, b)
