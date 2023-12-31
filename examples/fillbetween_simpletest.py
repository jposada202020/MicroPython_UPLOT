# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import gc
from machine import Pin, SPI
from ili9486 import ILI9486
from micropython_uplot.plot import PLOT
from micropython_uplot.utils import linspace
from micropython_uplot.fillbetween import Fillbetween

# Pin definition
pdc = Pin(8, Pin.OUT, value=0)
prst = Pin(15, Pin.OUT, value=1)
pcs = Pin(9, Pin.OUT, value=1)
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12), baudrate=30_000_000)
gc.collect()
display = ILI9486(spi, pcs, pdc, prst)

plot = PLOT(display, 5, 5, 300, 200, padding=1, box_color=(255, 255, 255))


x = list(linspace(0, 8, 25))

y1 = [value**2 / 2 for value in x]
y2 = [2 + value**2 + 3 * value for value in x]

Fillbetween(plot, x, y1, y2, fill_color=(255, 0, 0))

display.show()
