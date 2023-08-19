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
        ticksx: list = (0, 10, 30, 50, 70, 90),
        ticksy: list = (0, 10, 30, 50, 70, 90),
        tick_pos: bool = False,
        fill: bool = False,
    ) -> None:
        """

        :param Plot plot: Plot object for the scatter to be drawn
        :param list x: x points coordinates
        :param list y: y points coordinates
        :param list|None rangex: x range limits. Defaults to Nonem
        :param list|None rangey: y range limits. Defaults to None
        :param int|None line_color: line color. Defaults to None
        :param list ticksx: X axis ticks values
        :param list ticksy: Y axis ticks values
        :param bool tick_pos: indicates ticks position. True for below the axes.
         Defaults to ``False``
        :param bool fill: enable the filling of the plot. Defaults to ``False``

        """
        self.points = []
        self.ticksx = tuple(ticksx)
        self.ticksy = tuple(ticksy)

        self._pointer_index = plot._pointer_index

        self._line_color = set_color(
            plot._display,
            self._pointer_index,
            line_color[0],
            line_color[1],
            line_color[2],
        )
        plot._pointer_index += 1

        if tick_pos:
            self._tickposx = plot._tickheightx
            self._tickposy = plot._tickheighty
        else:
            self._tickposx = 0
            self._tickposy = 0

        self.xmin = rangex[0]
        self.xmax = rangex[1]
        self.ymin = rangey[0]
        self.ymax = rangey[1]

        self.draw_points(plot, x, y, fill)
        if plot._showticks:
            if plot._loggingfirst:
                plot._loggingfirst = False
                self._draw_ticks(plot)
                plot._showticks = False

    def _plot_line(self, plot: PLOT, index: int, xnorm: tuple, ynorm: tuple) -> None:
        plot._display.line(
            xnorm[index],
            ynorm[index],
            xnorm[index + 1],
            ynorm[index + 1],
            self._line_color,
        )

    def draw_points(self, plot: PLOT, x: list, y: list, fill: bool = False) -> None:
        """
        Draws points in the plot
        :param Plot plot: plot object provided
        :param list x: list of x values
        :param list y: list of y values
        :param bool fill: parameter to fill the plot graphic. Defaults to False
        :return: None
        """
        self.clear_plot(plot)
        # if self._limits:
        #     self._draw_limit_lines(plot)
        self.draw_new_lines(plot, x, y, fill)

    @staticmethod
    def clear_plot(plot: PLOT) -> None:
        """
        Clears the plot area
        :param PLOT plot: plot object provided
        """

        plot._display.rect(
            plot._newxmin + 1 + plot._tickheightx,
            plot._newymax + 1,
            plot._buff_width - 2 - 2 * plot.padding - plot._tickheightx,
            plot._buff_height - 2 - 2 * plot.padding - plot._tickheighty,
            plot._background_color,
            True,
        )

    def draw_new_lines(self, plot: PLOT, x: list, y: list, fill: bool = False) -> None:
        """
        Draw the plot lines
        :param PLOT plot: plot object provided
        :param list x: list of x values
        :param list y: list of y values
        :param bool fill: parameter to fill the plot graphic. Defaults to False
        :return: None
        """
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

        if len(x) == 1:
            plot._display.pixel(xnorm[0], ynorm[0], self._line_color)
        else:
            for index, _ in enumerate(xnorm):
                if index + 1 >= len(xnorm):
                    break
                if y[index] >= self.ymax:
                    continue

                self._plot_line(plot, index, xnorm, ynorm)

            if fill:
                for index, _ in enumerate(xnorm):
                    plot._display.line(
                        xnorm[index],
                        ynorm[index],
                        xnorm[index],
                        plot._newymin,
                        self._line_color,
                    )

    def _draw_ticks(self, plot) -> None:
        """
        Draw ticks in the plot area
        :param PLOT plot: plot object provided

        """

        ticksxnorm = tuple(
            [
                int(
                    plot.transform(
                        self.xmin, self.xmax, plot._newxmin, plot._newxmax, _
                    )
                )
                for _ in self.ticksx
            ]
        )
        ticksynorm = tuple(
            [
                int(
                    plot.transform(
                        self.ymin, self.ymax, plot._newymin, plot._newymax, _
                    )
                )
                for _ in self.ticksy
            ]
        )

        for i, tick in enumerate(ticksxnorm):
            plot._display.line(
                tick,
                plot._newymin,
                tick,
                plot._newymin - plot._tickheightx,
                plot._tickcolor,
            )
            if plot._showtext:
                plot.show_text(
                    "{:.{}f}".format(self.ticksx[i], plot._decimal_points),
                    tick,
                    plot._newymin,
                    ax="x",
                )

        for i, tick in enumerate(ticksynorm):
            plot._display.line(
                plot._newxmin,
                tick,
                plot._newxmin + plot._tickheighty,
                tick,
                plot._tickcolor,
            )
            if plot._showtext:
                plot.show_text(
                    "{:.{}f}".format(self.ticksy[i], plot._decimal_points),
                    plot._newxmin,
                    tick,
                    ax="y",
                )
