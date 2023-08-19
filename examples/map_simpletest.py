# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import gc
from math import pi, exp, sqrt
from random import choice
from machine import Pin, SPI
import array
from ili9486 import ILI9486
from micropython_uplot.plot import PLOT
from micropython_uplot.utils import linspace
from micropython_uplot.map import Map

# Pin definition
pdc = Pin(8, Pin.OUT, value=0)
prst = Pin(15, Pin.OUT, value=1)
pcs = Pin(9, Pin.OUT, value=1)
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12), baudrate=30_000_000)
gc.collect()
display = ILI9486(spi, pcs, pdc, prst)

plot = PLOT(display, 5, 5, 300, 250, padding=1, box_color=(255, 255, 255))

# Setting some date to plot
x = linspace(-4, 4, 100)
y = tuple([(2.0 / sqrt(2 * pi) * exp((-(value**2)) / 4.0)) for value in x])
ymax = max(y)

y1 = []

rows, cols = (10, 10)
indice = 0

for i in range(rows):
    col = []
    for j in range(cols):
        col.append(y[indice])
        indice += 1
    y1.append(col)


# Plotting and showing the plot
Map(plot, y1, ymax, [rows, cols], (255, 0, 68), (68, 0, 255))
# Plotting and showing the plot
display.show()
