# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import gc
import math
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

plot = PLOT(display, 5, 5, 300, 250, padding=1, box_color=(255, 255, 255))
plot.tick_params(
    tickx_height=12, ticky_height=12, tickcolor=(100, 100, 100), tickgrid=True
)

# Creating some points to graph
x = list(linspace(-4, 4, 50))
constant = 1.0 / math.sqrt(2 * math.pi)
y = [constant * math.exp((-(_**2)) / 2.0) for _ in x]
y2 = [constant / 2 * math.exp((-(_**2)) / 1.0) for _ in x]
y3 = [10 + (2 + constant / 1.1 * math.exp((-(_**2)) / 0.5 + 2)) for _ in x]
# Drawing the graph
Cartesian(plot, x, y, line_color=(255, 255, 0), line_style=".")
Cartesian(plot, x, y2, line_color=(0, 255, 0), line_style="-.-")
p = Cartesian(plot, x, y3, line_color=(0, 255, 255), line_style="- -")
display.show()
import time

time.sleep(1)
# plot._savingppm("line_types.ppm")
p.update(plot)
display.show()
