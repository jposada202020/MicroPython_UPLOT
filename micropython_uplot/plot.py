# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`plot`
================================================================================

MicroPython Graphics Library


* Author: Jose D. Montoya


"""

from micropython_uplot.colors import set_color

try:
    from typing import Union, Optional
    from typing_extensions import Literal
except ImportError:
    pass


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/MicroPython_UPLOT.git"


class PLOT:
    """
    Canvas Class to add different elements to the screen.
    The origin point set by ``x`` and ``y`` properties

    :param display: display object
    :param int x: origin x coordinate
    :param int y: origin y coordinate
    :param int width: plot box width in pixels
    :param int height: plot box height in pixels
    :param int padding: padding for the plot box in all directions
    :param bool show_box: select if the plot box is displayed
    :param tuple background_color: background color. Defaults to black ``(0, 0, 0)``
    :param tuple box_color: allows to choose the box line color.
     Defaults to white ''(255, 255, 255)``
    :param int tickx_height: x axes tick height in pixels. Defaults to 8.
    :param int ticky_height: y axes tick height in pixels. Defaults to 8.

    """

    def __init__(
        self,
        display,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 100,
        padding: int = 25,
        show_box: bool = True,
        background_color: int = (0, 0, 0),
        box_color: tuple = (255, 255, 255),
        tickx_height: int = 8,
        ticky_height: int = 8,
    ) -> None:
        self._display = display
        self._background_color = set_color(
            display, 0, background_color[0], background_color[1], background_color[2]
        )

        self._tickcolor = set_color(display, 1, 255, 255, 255)
        self._boxcolor = set_color(display, 2, box_color[0], box_color[1], box_color[2])
        self._color0 = background_color
        self._color1 = box_color
        self._color2 = (255, 255, 255)

        self._axesparams = "box"
        self._decimal_points = None
        self._buff_width = width
        self._buff_height = height

        self._width = x + width
        self._height = y + height

        self.padding = padding
        self._newxmin = x + padding
        self._newxmax = x + width - padding - 1

        self._newymin = y + height - padding - 1
        self._newymax = y + padding

        self._cartesianfirst = True
        self._loggingfirst = True
        self._scatterfirst = True
        self._showtext = False

        self._tickheightx = tickx_height
        self._tickheighty = ticky_height

        self._showticks = False
        self._tickgrid = False

        self._grid_espace = 2
        self._grid_lenght = 2

        self._index_colorused = 4

        self._pointer_index = 3

        if show_box:
            self._drawbox()

    def _drawbox(self) -> None:
        """
        Draw the plot box

        :return: None

        """
        # self._display.fill(self._background_color)

        if self._axesparams == "cartesian":
            draw_box = [True, True, False, False]
        elif self._axesparams == "line":
            draw_box = [False, True, False, False]
        else:
            draw_box = [True, True, True, True]

        # left y axes line
        if draw_box[0]:
            # y axes line
            self._display.line(
                self._newxmin,
                self._newymax,
                self._newxmin,
                self._height - self.padding - 1,
                self._boxcolor,
            )
        # bottom x axes line
        if draw_box[1]:
            self._display.line(
                self._newxmin,
                self._height - self.padding - 1,
                self._width - self.padding - 1,
                self._height - self.padding - 1,
                self._boxcolor,
            )
        # right y axes line
        if draw_box[2]:
            self._display.line(
                self._width - self.padding - 1,
                self._newymax,
                self._width - self.padding - 1,
                self._height - self.padding - 1,
                self._boxcolor,
            )
        # top x axes line
        if draw_box[3]:
            self._display.line(
                self._newxmin,
                self._newymax,
                self._width - self.padding - 1,
                self._newymax,
                self._boxcolor,
            )

    def _update_plot(self) -> None:
        """
        Function to update graph

        :return: None

        """

        self._drawbox()

    def axs_params(self, axstype: Literal["box", "cartesian", "line"] = "box") -> None:
        """
        Setting up axs visibility

        :param str axstype: argument with the kind of axs you selected

        :return: None

        """
        self._axesparams = axstype
        self._update_plot()

    def _draw_ticks(self, x: int, y: int, ticksx=None, ticksy=None) -> None:
        """
        Draw ticks in the plot area

        :param int x: x coord
        :param int y: y coord
        :param list[int] ticksx: x ticks data. Defaults to None
        :param list[int] ticksy: y ticks data. Defaults to None

        :return:None

        """
        ticks_dummy = (10, 30, 50, 70, 90)
        subticks_dummy = (20, 40, 60, 80)
        minx = min(x)
        maxx = max(x)
        miny = min(y)
        maxy = max(y)

        if ticksx is None:
            ticksxnorm = tuple(
                [self.transform(0, 100, minx, maxx, _) for _ in ticks_dummy]
            )
            subticksxnorm = tuple(
                [self.transform(0, 100, minx, maxx, _) for _ in subticks_dummy]
            )
        else:
            ticksxnorm = tuple([self.transform(0, 100, minx, maxx, _) for _ in ticksx])

        if ticksy is None:
            ticksynorm = tuple(
                [self.transform(0, 100, miny, maxy, _) for _ in ticks_dummy]
            )
            subticksynorm = tuple(
                [self.transform(0, 100, miny, maxy, _) for _ in subticks_dummy]
            )
        else:
            ticksynorm = tuple([self.transform(0, 100, miny, maxy, _) for _ in ticksy])

        ticksxrenorm = tuple(
            [
                int(self.transform(minx, maxx, self._newxmin, self._newxmax, _))
                for _ in ticksxnorm
            ]
        )
        ticksyrenorm = tuple(
            [
                int(self.transform(miny, maxy, self._newymin, self._newymax, _))
                for _ in ticksynorm
            ]
        )

        if ticksx is None:
            subticksxrenorm = tuple(
                [
                    int(self.transform(minx, maxx, self._newxmin, self._newxmax, _))
                    for _ in subticksxnorm
                ]
            )
        if ticksy is None:
            subticksyrenorm = tuple(
                [
                    int(self.transform(miny, maxy, self._newymin, self._newymax, _))
                    for _ in subticksynorm
                ]
            )

        for i, tick in enumerate(ticksxrenorm):
            self._display.line(
                tick,
                self._newymin,
                tick,
                self._newymin - self._tickheightx,
                self._tickcolor,
            )
            if self._showtext:
                self.show_text(
                    "{:.{}f}".format(ticksxnorm[i], self._decimal_points),
                    tick,
                    self._newymin,
                    ax="x",
                )

        for i, tick in enumerate(ticksyrenorm):
            self._display.line(
                self._newxmin,
                tick,
                self._newxmin + self._tickheighty,
                tick,
                self._tickcolor,
            )
            if self._showtext:
                self.show_text(
                    "{:.{}f}".format(ticksynorm[i], self._decimal_points),
                    self._newxmin,
                    tick,
                    ax="y",
                )

        if ticksx is None:
            for tick in subticksxrenorm:
                self._display.line(
                    tick,
                    self._newymin,
                    tick,
                    self._newymin - self._tickheightx // 2,
                    self._tickcolor,
                )

        if ticksy is None:
            for tick in subticksyrenorm:
                self._display.line(
                    self._newxmin,
                    tick,
                    self._newxmin + self._tickheighty // 2,
                    tick,
                    self._tickcolor,
                )

        if self._tickgrid:
            self._draw_gridx(ticksxrenorm)
            self._draw_gridy(ticksyrenorm)

    @staticmethod
    def transform(
        oldrangemin: Union[float, int],
        oldrangemax: Union[float, int],
        newrangemin: Union[float, int],
        newrangemax: Union[float, int],
        value: Union[float, int],
    ) -> Union[float, int]:
        """
        This function converts the original value into a new defined value in the new range

        :param int|float oldrangemin: minimum of the original range
        :param int|float oldrangemax: maximum of the original range
        :param int|float newrangemin: minimum of the new range
        :param int|float newrangemax: maximum of the new range
        :param int|float value: value to be converted

        :return int|float: converted value

        """
        return (
            ((value - oldrangemin) * (newrangemax - newrangemin))
            / (oldrangemax - oldrangemin)
        ) + newrangemin

    def tick_params(
        self,
        show_ticks=True,
        tickx_height: int = 8,
        ticky_height: int = 8,
        tickcolor: int = (255, 255, 255),
        tickgrid: bool = False,
        showtext: bool = False,
        decimal_points: int = 0,
    ) -> None:
        """
        Function to set ticks parameters

        :param bool show_ticks: Show ticks. Defaults to `True`
        :param int tickx_height: X axes tick height in pixels. Defaults to 8
        :param int ticky_height: Y axes tick height in pixels. Defaults to 8
        :param int tickcolor: tick color in hex. Defaults to white. ``0xFFFFFF``
        :param bool tickgrid: defines if the grid is to be shown. Defaults to `False`
        :param bool showtext: Show Axes text. Defaults to `False`
        :param int decimal_points: Number of decimal points to show. Defaults to :const:`0`

        :return: None

        """
        if showtext and self.padding < 20:
            raise ValueError(
                "Please select a padding that allows to show the tick text"
            )

        self._showticks = show_ticks
        self._tickheightx = tickx_height
        self._tickheighty = ticky_height

        self._tickcolor = set_color(
            self._display, 1, tickcolor[0], tickcolor[1], tickcolor[2]
        )
        self._color2 = tickcolor

        self._tickgrid = tickgrid
        self._showtext = showtext
        self._decimal_points = decimal_points

    def show_text(
        self,
        text: str,
        x: int,
        y: int,
        text_color: Optional[int] = None,
        free_text: bool = False,
        ax=None,
    ) -> None:
        """
        Show desired text in the screen
        :param str text: text to be displayed
        :param int x: x coordinate
        :param int y: y coordinate
        :param int color: text color. Defaults to None
        :param bool free_text: Select to show free text
        :return: None
        """

        font_height = 8
        font_width = 8
        distance = 5

        if ax == "y":
            x = x - font_width * (len(text)) - distance
            y = y - font_height // 2
        if ax == "x":
            x = x - font_width // 2
            y = y + font_height

        if text_color is None:
            text_color = self._tickcolor

        if self._showtext or free_text:
            self._display.text(text, x, y, text_color)

    def _draw_gridy(self, ticks_data: list[int]) -> None:
        """
        Draws plot grid in the y axs

        :param list[int] ticks_data: ticks data information

        :return: None

        """
        for tick in ticks_data:
            start = self._newxmin
            while start + self._grid_lenght <= self._newxmax:
                self._display.line(
                    start,
                    tick,
                    start + self._grid_lenght,
                    tick,
                    self._tickcolor,
                )
                start = start + self._grid_espace + self._grid_lenght

    def _draw_gridx(self, ticks_data: list[int]) -> None:
        """
        Draws the plot grid

        :param list[int] ticks_data: ticks data information

        :return: None

        """
        for tick in ticks_data:
            start = self._newymin
            while start - self._grid_lenght - self._grid_espace >= self._newymax:
                self._display.line(
                    tick,
                    start,
                    tick,
                    start - self._grid_lenght,
                    self._tickcolor,
                )
                start = start - self._grid_espace - self._grid_lenght

    def _writeplainpbm(self, file: str = "newfile.pbm") -> None:
        """
        Function to write a plain pbm file
        adapted from https://github.com/orgs/micropython/discussions/10785
        Author: Stewart Russell
        """
        with open(file, "wb") as file_write:
            file_write.write("P1" + "\n")
            file_write.write(str(480) + " " + str(320) + "\n")
            for y in range(320):
                for x in range(480):
                    file_write.write(str(self._display.pixel(x, y)))
                file_write.write("\n")
            file_write.close()

    def _savingppm(
        self, filename: str = "picture.ppm", width: int = 480, height: int = 320
    ) -> None:
        """
        Function to save the screen as a ppm file
        Adapted from https://gist.github.com/nicholasRutherford/c95a55239e03ba99bab3
        Author: Nicholas Rutherford

        :param str filename: picture filename
        :param int width: screenshot width in pixels
        :param int height: screenshot height in pixels

        This function requires adding the colors used manually in the z list
        """

        z = [
            self._color0,
            self._color2,
            self._color1,
            self._color0,
            (237, 0, 86),
            (218, 0, 105),
            (199, 0, 124),
            (181, 0, 142),
            (162, 0, 161),
            (143, 0, 180),
            (125, 0, 198),
            (106, 0, 217),
            (87, 0, 236),
            (68, 0, 255),
        ]

        # Header values for the file
        comment = b"MicroPlot"
        ftype = b"P6"

        # First write the header values
        with open(filename, "wb+") as ppmfile:
            ppmfile.write(b"%s\n" % (ftype))
            ppmfile.write(b"#%s\n" % comment)
            ppmfile.write(b"%d %d\n" % (width, height))
            ppmfile.write(b"255\n")

            for y in range(height):
                for x in range(width):
                    ppmfile.write(
                        b"%c%c%c"
                        % (
                            z[self._display.pixel(x, y)][0],
                            z[self._display.pixel(x, y)][1],
                            z[self._display.pixel(x, y)][2],
                        )
                    )
            ppmfile.close()
