# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

"""

`cartesian`
================================================================================

MicroPython cartesian graph

* Author: Jose D. Montoya


"""
try:
    from typing import Optional
    from micropython_uplot.plot import PLOT
except ImportError:
    pass

from array import array
from micropython_uplot.colors import set_color


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/MicroPython_UPLOT.git"


class Cartesian:
    """
    Class to draw cartesian plane
    """

    def __init__(
        self,
        plot: PLOT,
        x: list,
        y: list,
        rangex: Optional[list] = None,
        rangey: Optional[list] = None,
        line_color: tuple = (0, 255, 0),
        line_style: Optional[str] = None,
        ticksx: list = None,
        ticksy: list = None,
        fill: bool = False,
        pointer_index: Optional[int] = None,
    ) -> None:
        """

        :param Plot plot: Plot object for the scatter to be drawn
        :param list x: x points coordinates
        :param list y: y points coordinates
        :param list|None rangex: x range limits. Defaults to None
        :param list|None rangey: y range limits. Defaults to None
        :param int|None line_color: line color. Defaults to None
        :param str|None line_style: line style. Defaults to None
        :param list ticksx: X axis ticks values
        :param list ticksy: Y axis ticks values
        :param bool fill: Show the filling. Defaults to `False`
        :param int|None pointer_index: Pointer index. Defaults to None

        """
        self.points = []
        self.ticksx = ticksx
        self.ticksy = ticksy

        if pointer_index is None:
            self._pointer_index = plot._pointer_index
        else:
            self._pointer_index = pointer_index

        self._line_color = set_color(
            plot._display,
            self._pointer_index,
            line_color[0],
            line_color[1],
            line_color[2],
        )
        plot._pointer_index += 1

        if line_style is None:
            self._line_type = "-"
        else:
            self._line_type = line_style

        if self._line_type not in ["-", ".", "- -", "-.-"]:
            raise ValueError("line_style must be a valid option")

        max_x = max(x)
        min_x = min(x)
        max_y = max(y)
        min_y = min(y)

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

        xnorm = tuple(
            [
                int(
                    plot.transform(
                        self.xmin, self.xmax, plot._newxmin, plot._newxmax, _
                    )
                )
                for _ in x
            ]
        )
        ynorm = tuple(
            [
                int(
                    plot.transform(
                        self.ymin, self.ymax, plot._newymin, plot._newymax, _
                    )
                )
                for _ in y
            ]
        )

        if fill:
            self.points.extend([xnorm[0], plot._newymin])
            for index, item in enumerate(xnorm):
                self.points.extend([item, ynorm[index]])
            self.points.extend([xnorm[-1], plot._newymin])
            self.points.extend([xnorm[0], plot._newymin])
            array_points = array("i", self.points)
            plot._display.poly(0, 0, array_points, self._line_color, True)

        for index, _ in enumerate(xnorm):
            if index + 1 >= len(xnorm):
                break
            if y[index] >= self.ymax:
                continue

            self._draw_plotline(plot, index, xnorm, ynorm)

        if plot._showticks:
            if plot._cartesianfirst:
                plot._draw_ticks(x, y, self.ticksx, self.ticksy)
                plot._cartesianfirst = False
                plot._showticks = False

    def _draw_plotline(
        self, plot: PLOT, index: int, xnorm: tuple, ynorm: tuple
    ) -> None:
        """
        Draw plot line
        :param PLOT plot: plot object provided
        :param int index: index of the point to be drawn
        :param tuple xnorm: x points coordinates
        :param tuple ynorm: y points coordinates
        """
        if self._line_type == "-":
            self._plot_line(plot, index, xnorm, ynorm)
        elif self._line_type == "-.-":
            if index % 3 == 0:
                self._plot_line(plot, index, xnorm, ynorm)
            else:
                plot._display.pixel(xnorm[index], ynorm[index], self._line_color)
        elif self._line_type == ".":
            plot._display.pixel(xnorm[index], ynorm[index], self._line_color)
        elif self._line_type == "- -":
            if index % 2 == 0:
                self._plot_line(plot, index, xnorm, ynorm)

    def _plot_line(self, plot: PLOT, index: int, xnorm: tuple, ynorm: tuple) -> None:
        """
        Draw plot line
        :param PLOT plot: plot object provided
        :param int index: index of the point to be drawn
        :param tuple xnorm: x points coordinates
        :param tuple ynorm: y points coordinates
        """
        plot._display.line(
            xnorm[index],
            ynorm[index],
            xnorm[index + 1],
            ynorm[index + 1],
            self._line_color,
        )


class LineStyle:
    """
    Line style class
    """

    SOLID = "-"
    DASHED = "- -"
    DASH_DOT = "-.-"
    DOTTED = "."
