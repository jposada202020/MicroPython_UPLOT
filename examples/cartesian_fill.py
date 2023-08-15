# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import gc
from machine import Pin, SPI
from ili9486 import ILI9486
from micropython_uplot.plot import PLOT
from micropython_uplot.utils import linspace
from micropython_uplot.cartesian import Cartesian

# Pin definition
pdc = Pin(8, Pin.OUT, value=0)
prst = Pin(15, Pin.OUT, value=1)
pcs = Pin(9, Pin.OUT, value=1)
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12), baudrate=30_000_000)
gc.collect()
display = ILI9486(spi, pcs, pdc, prst)

plot = PLOT(display, 5, 5, 460, 150, padding=1, box_color=(255, 255, 255))
plot.tick_params(
    tickx_height=12, ticky_height=12, tickcolor=(100, 100, 100), tickgrid=True
)

# Creating some points to graph
x = list(linspace(0, 4, 25))
y = [value * (value - 2) ** 2 for value in x]

# Drawing the graph
Cartesian(plot, x, y, rangey=[-1, 18], line_color=(255, 89, 0), fill=True)

display.show()
