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
    
    c = ssd.rgb(r, g, b)

    x = idx << 1
    ssd.lut[x] = c & 0xff
    ssd.lut[x + 1] = c >> 8
    return idx


def set_color(display, idx, r, g, b):
    if hasattr(display, 'lut'):
        return create_color(display, idx, r, g, b)
    else:
        return display.rgb(r, g, b)
