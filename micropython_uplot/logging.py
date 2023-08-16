# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

"""

`logging`
================================================================================

MicroPython logging utility

* Author: Jose D. Montoya


"""
try:
    from typing import Optional
    from micropython_uplot.plot import PLOT
except ImportError:
    pass

from micropython_uplot.colors import set_color


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/MicroPython_UPLOT.git"


class Logging:
    """
    Class to log data
    """

    def __init__(
        self,
        plot: PLOT,
        x: list,
        y: list,
        rangex: Optional[list] = None,
        rangey: Optional[list] = None,
        line_color: tuple = (0, 255, 0),
        ticksx: list = None,
        ticksy: list = None,
    ) -> None:
        """

        :param Plot plot: Plot object for the scatter to be drawn
        :param list x: x points coordinates
        :param list y: y points coordinates
        :param list|None rangex: x range limits. Defaults to None
        :param list|None rangey: y range limits. Defaults to None
        :param int|None line_color: line color. Defaults to None
        :param list ticksx: X axis ticks values
        :param list ticksy: Y axis ticks values

        """
        self.points = []
        self.ticksx = ticksx
        self.ticksy = ticksy

        self._line_color = set_color(
            plot._display,
            self._pointer_index,
            line_color[0],
            line_color[1],
            line_color[2],
        )
        plot._pointer_index += 1

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

    def _plot_line(self, plot, index, xnorm, ynorm):
        plot._display.line(
            xnorm[index],
            ynorm[index],
            xnorm[index + 1],
            ynorm[index + 1],
            self._line_color,
        )

    def update(self, plot):
        """
        Update the plot with new data
        """
        plot._display.fill(0)
