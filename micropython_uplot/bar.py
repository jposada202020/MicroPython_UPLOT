# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

"""

`bar`
================================================================================

MicroPython bar graph

* Author: Jose D. Montoya


"""

try:
    from micropython_uplot.plot import PLOT
except ImportError:
    pass
from math import ceil
from micropython_uplot.colors import set_color

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/CircuitPython_uplot.git"

# pylint: disable=protected-access
# pylint: disable=no-self-use


class Bar:
    """
    Main class to display different graphics
    """

    def __init__(
        self,
        plot: PLOT,
        x: list,
        y: list,
        fill: bool = False,
        bar_space=16,
        xstart=50,
        color_palette=None,
        max_value=None,
    ) -> None:
        """
        :param Plot plot: Plot object for the scatter to be drawn
        :param list x: x data
        :param list y: y data
        :param bool fill: boxes fill attribute. Defaults to `False`
        :param int bar_space: space in pixels between the bars
        :param int xstart: start point in the x axis for the bar to start. Defaults to :const:`50`
        :param list color_palette: list of colors to be used for the bars. Defaults to None.
         Be aware that you need to include the same number if colors as your data.
         This functionality will only work with filled bars.
        :param int max_value: for filled unprojected bars will setup the maxium value for the bars.
         This allows the user to update the bars in real-time. There is an example in the examples
         folder showing this functionality

        """
        self._plot_obj = plot
        self._filled = fill
        self._plot_palette = []
        self._plot_palette.append((20, 159, 20))
        self._plot_palette.append((100, 113, 130))
        self._plot_palette.append((116, 40, 239))
        self._plot_palette.append((0, 94, 153))
        self._plot_palette.append((0, 167, 109))
        self._plot_palette.append((44, 73, 113))
        self._color = []

        if color_palette is None:
            for element in self._plot_palette:
                self._color.append(
                    set_color(
                        plot._display,
                        plot._pointer_index,
                        element[0],
                        element[1],
                        element[2],
                    )
                )
                plot._pointer_index += 1
        else:
            for element in color_palette:
                self._color.append(
                    set_color(
                        plot._display,
                        plot._pointer_index,
                        element[0],
                        element[1],
                        element[2],
                    )
                )
                plot._pointer_index += 1

        self._y = y

        if max_value is None:
            y_max = max(y)
        else:
            y_max = max_value

        xstart = plot._newxmin + xstart + bar_space

        self._graphx = ceil(abs(plot._newxmax - plot._newxmin) / (len(x) + 4))
        self._graphy = abs(plot._newymax - plot._newymin) / (y_max + 2)

        self._new_min = int(plot.transform(0, y_max, y_max, 0, 0))
        self._new_max = int(plot.transform(0, y_max, y_max, 0, y_max))

        for i, _ in enumerate(x):
            self._create_bars(plot, xstart, i)
            xstart = xstart + bar_space

    def _create_bars(self, plot, xstart: int, indice: int):
        """
        create plot bars
        """

        plot._display.rect(
            xstart + (indice * self._graphx),
            int(self._plot_obj._newymin - self._graphy * self._y[indice]),
            self._graphx,
            ceil(self._graphy * self._y[indice]),
            self._color[indice],
            True,
        )
