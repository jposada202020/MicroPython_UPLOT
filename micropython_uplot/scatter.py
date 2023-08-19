# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`scatter`
================================================================================

scatter plot for micropython_uplot


* Author: Jose D. Montoya


"""
from array import array
from micropython_uplot.colors import set_color

try:
    from typing import Union, Optional
    from micropython_uplot.plot import PLOT
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/MicroPython_UPLOT.git"


_TRIANGLE = array("i", [0, 0, 8, 0, 4, -7])
_SQUARE = array("i", [0, 0, 6, 0, 6, -6, 0, -6])
_DIAMOND = array("i", [0, 0, 3, -4, 6, 0, 3, 4])


class Scatter:
    """
    Main class to display different graphics
    """

    def __init__(
        self,
        plot: PLOT,
        x: list,
        y: list,
        rangex: Optional[list] = None,
        rangey: Optional[list] = None,
        radius: Optional[Union[list, int]] = 3,
        pointer_color: tuple = (0, 255, 0),
        pointer: Optional[str] = None,
        pointer_index: Optional[int] = None,
    ) -> None:
        """

        :param plot: Plot object for the scatter to be drawn
        :param x: x points coordinates
        :param y: y points coordinates
        :param list|None rangex: x range limits
        :param list|None rangey: y range limits
        :param int|list radius: circle radius
        :param int pointer_color: pointer color. Default is 0xFF905D
        :param str|None pointer: pointer shape.
        :param int|None pointer_index: pointer index. Default is None

        """

        if pointer is None:
            self._pointer = "circle"
        else:
            self._pointer = pointer

        if pointer_index is None:
            self._pointer_index = plot._pointer_index
        else:
            self._pointer_index = pointer_index

        self._radius = radius
        self._pointer_color = set_color(
            plot._display,
            self._pointer_index,
            pointer_color[0],
            pointer_color[1],
            pointer_color[2],
        )
        plot._pointer_index += 1

        if isinstance(self._radius, list) and self._pointer != "circle":
            raise ValueError(
                f"Pointer paramater is {self._pointer}. Variable Radius are not accepted"
            )

        max_x = max(x)
        min_x = min(x)
        max_y = max(y)
        min_y = min(y)

        if rangex is None:
            xmin = min_x - (abs(max_x - min_x) / 10)
            xmax = max_x + (abs(max_x - min_x) / 10)
        else:
            xmin = min(rangex)
            xmax = max(rangex)

        if rangey is None:
            ymin = min_y - (abs(max_y - min_y) / 10)
            ymax = max_y + (abs(max_y - min_y) / 10)
        else:
            ymin = min(rangey)
            ymax = max(rangey)

        self._xnorm = tuple(
            [
                int(plot.transform(xmin, xmax, plot._newxmin, plot._newxmax, _))
                for _ in x
            ]
        )
        self._ynorm = tuple(
            [
                int(plot.transform(ymin, ymax, plot._newymin, plot._newymax, _))
                for _ in y
            ]
        )

        self._draw_pointer(plot)

        if plot._scatterfirst:
            if plot._showticks:
                plot._draw_ticks(x, y)

                plot._scatterfirst = False
                plot._showticks = False

    def _draw_pointer(self, plot: PLOT) -> None:
        """

        :param PLOT plot: Plot object for the scatter to be drawn

        """

        if isinstance(self._radius, list):
            for i, _ in enumerate(self._xnorm):
                plot._display.ellipse(
                    self._xnorm[i],
                    self._ynorm[i],
                    self._radius[i],
                    self._radius[i],
                    self._pointer_color,
                    True,
                )

        else:
            for i, _ in enumerate(self._xnorm):
                if self._pointer == "circle":
                    plot._display.ellipse(
                        self._xnorm[i],
                        self._ynorm[i],
                        self._radius,
                        self._radius,
                        self._pointer_color,
                        True,
                    )

                elif self._pointer == "triangle":
                    plot._display.poly(
                        self._xnorm[i],
                        self._ynorm[i],
                        _TRIANGLE,
                        self._pointer_color,
                        True,
                    )

                elif self._pointer == "square":
                    plot._display.poly(
                        self._xnorm[i],
                        self._ynorm[i],
                        _SQUARE,
                        self._pointer_color,
                        True,
                    )
                elif self._pointer == "diamond":
                    plot._display.poly(
                        self._xnorm[i],
                        self._ynorm[i],
                        _DIAMOND,
                        self._pointer_color,
                        True,
                    )


class Pointer:
    """
    Pointer container class
    """

    CIRCLE = "circle"
    TRIANGLE = "triangle"
    SQUARE = "square"
    DIAMOND = "diamond"
