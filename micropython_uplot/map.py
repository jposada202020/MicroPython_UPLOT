# SPDX-FileCopyrightText: 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT


"""

`map`
================================================================================

MicroPython color map graph

* Author: Jose D. Montoya


"""
try:
    from micropython_uplot.plot import PLOT
except ImportError:
    pass

from math import floor
from micropython_uplot.colors import set_color

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/MicrotPython_UPLOT.git"


class Map:
    """
    Main class to display different graphics
    """

    def __init__(
        self,
        plot: PLOT,
        data_points: list,
        data_points_max: float,
        matrix_shape: list,
        initial_color: tuple,
        final_color: tuple,
    ) -> None:
        """
        Due to IL9436 Display driver limitations number of map colors is limited to 10
        :param PLOT plot: Plot object for the scatter to be drawn
        :param list data_points: data points to create the color map
        :param float data_points_max: data points max value
        :param list matrix_shape: data_points matrix shape
        :param tuple initial_color: initial color to create the color map
        :param tuple final_color: final color to create the color map

        """

        self._numbins = 10

        self._pointer_index = 3
        self._step = data_points_max / self._numbins

        width = plot._newxmax - plot._newxmin
        height = plot._newymin - plot._newymax
        xdist = width // matrix_shape[0]
        ydist = height // matrix_shape[1]

        for i in range(1, 11):
            color = color_fade(initial_color, final_color, i / 10)
            print(color)
            set_color(
                plot._display,
                self._pointer_index + i,
                color[0],
                color[1],
                color[2],
            )

        deltax = plot._newxmin + plot.padding
        deltay = plot._newymax + plot.padding

        for i, row in enumerate(data_points):
            for j, col in enumerate(row):
                if floor(col / self._step) > 9:
                    color = 9
                else:
                    color = floor(col / self._step)
                plot._display.rect(
                    deltax,
                    deltay,
                    xdist,
                    ydist,
                    self._pointer_index + color + 1,
                    True,
                )
                deltax = deltax + xdist
            deltax = plot._newxmin + plot.padding
            deltay = deltay + ydist


def color_fade(start_color: int, end_color: int, fraction: float):
    """Linear extrapolation of a color between two RGB colors (tuple or 24-bit integer).

    :param start_color: starting color
    :param end_color: ending color
    :param fraction: Floating point number  ranging from 0 to 1 indicating what
     fraction of interpolation between start_color and end_color.

    """

    if fraction >= 1:
        return end_color
    if fraction <= 0:
        return start_color

    faded_color = [0, 0, 0]
    for i in range(3):
        faded_color[i] = start_color[i] - int(
            (start_color[i] - end_color[i]) * fraction
        )
    return faded_color
