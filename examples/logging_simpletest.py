# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import gc
import math
from machine import Pin, SPI
from ili9486 import ILI9486
from micropython_uplot.plot import PLOT
from micropython_uplot.utils import linspace
from micropython_uplot.logging import Logging

# Pin definition
pdc = Pin(8, Pin.OUT, value=0)
prst = Pin(15, Pin.OUT, value=1)
pcs = Pin(9, Pin.OUT, value=1)
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12), baudrate=30_000_000)
gc.collect()
display = ILI9486(spi, pcs, pdc, prst)

plot = PLOT(display, 5, 5, 300, 250, padding=1, box_color=(255, 255, 255))

x = list(linspace(-4, 4, 25))
constant = 1.0 / math.sqrt(2 * math.pi)
y = [constant * math.exp((-(_**2)) / 2.0) for _ in x]
# Drawing the graph
my_log = Logging(plot, x, y, rangex=[-4, 4], rangey=[0, 1], line_color=(255, 255, 0))

display.show()
