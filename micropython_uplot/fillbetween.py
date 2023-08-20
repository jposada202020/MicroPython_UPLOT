# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

"""

`fillbetween`
================================================================================

MicroPython fillbetween graph

* Author: Jose D. Montoya


"""
try:
    from typing import Optional, Union
    from micropython_uplot.plot import PLOT
except ImportError:
    pass

from array import array
from micropython_uplot.colors import set_color


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/MicroPython_UPLOT.git"


class Fillbetween:
    """
    Class to draw a fillbetween graph
    """

    def __init__(
        self,
        plot: PLOT,
        x: list,
        y1: list,
        y2: list,
        rangex: Optional[list] = None,
        rangey: Optional[list] = None,
        fill_color: int = (0, 255, 0),
        pointer_index: Optional[int] = None,
    ) -> None:
        """
        :param Plot plot: Plot object for the scatter to be drawn
        :param list x: x points coordinates
        :param list y1: y1 points coordinates
        :param list y2: y2 points coordinates
        :param list|None rangex: x range limits
        :param list|None rangey: y range limits
        :param int fill_color: filling color. Defaults to (0, 255, 0)
        :param int|None pointer_index: Pointer index. Defaults to None

        """

        if pointer_index is None:
            self._pointer_index = plot._pointer_index
        else:
            self._pointer_index = pointer_index

        self._line_color = set_color(
            plot._display,
            self._pointer_index,
            fill_color[0],
            fill_color[1],
            fill_color[2],
        )
        plot._pointer_index += 1

        points = []

        max_x = max(x)
        min_x = min(x)
        max_y = max(max(y2), max(y1))
        min_y = min(min(y1), min(y2))

        if rangex is None:
            self.xmin = min_x - (abs(max_x - min_x) / 10)
            self.xmax = max_x + (abs(max_x - min_x) / 10)

        else:
            self.xmin = min(rangex)
            self.xmax = max(rangex)

        if rangey is None:
            self.ymin = min_y - (abs(max_y - min_y) / 10)
            self.ymax = max_y + (abs(max_y - min_y) / 10)
        else:
            self.ymin = min(rangey)
            self.ymax = max(rangey)

        xnorm = [
            int(plot.transform(self.xmin, self.xmax, plot._newxmin, plot._newxmax, _))
            for _ in x
        ]
        xrev = [
            int(plot.transform(self.xmin, self.xmax, plot._newxmin, plot._newxmax, _))
            for _ in x
        ]

        xrev.reverse()

        y1norm = tuple(
            [
                int(
                    plot.transform(
                        self.ymin, self.ymax, plot._newymin, plot._newymax, _
                    )
                )
                for _ in y1
            ]
        )
        y2norm = [
            int(plot.transform(self.ymin, self.ymax, plot._newymin, plot._newymax, _))
            for _ in y2
        ]
        y2norm.reverse()

        flip2y = y2norm

        for index, item in enumerate(xnorm):
            points.extend([item, y1norm[index]])
        for index, item in enumerate(xrev):
            points.extend([item, flip2y[index]])

        array_points = array("i", points)
        plot._display.poly(0, 0, array_points, self._line_color, True)
