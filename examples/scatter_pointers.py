# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import gc
from random import choice
from machine import Pin, SPI
from ili9486 import ILI9486
from micropython_uplot.plot import PLOT
from micropython_uplot.utils import linspace
from micropython_uplot.scatter import Scatter, Pointer

# Pin definition
pdc = Pin(8, Pin.OUT, value=0)
prst = Pin(15, Pin.OUT, value=1)
pcs = Pin(9, Pin.OUT, value=1)
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12), baudrate=30_000_000)
gc.collect()
display = ILI9486(spi, pcs, pdc, prst)

plot = PLOT(display, 0, 0, display.width // 2, display.height // 2, padding=1)
plot2 = PLOT(display, 240, 0, display.width // 2, display.height // 2, padding=1)
plot3 = PLOT(display, 0, 160, display.width // 2, display.height // 2, padding=1)
plot4 = PLOT(display, 240, 160, display.width // 2, display.height // 2, padding=1)

# Creating some Data
a = list(linspace(1, 100, 100))
b = [choice(a) for _ in a]
Scatter(plot, a, b, pointer_index=4)
Scatter(
    plot2, a, b, pointer=Pointer.TRIANGLE, pointer_color=(255, 255, 94), pointer_index=5
)
Scatter(
    plot3, a, b, pointer=Pointer.SQUARE, pointer_color=(255, 255, 255), pointer_index=6
)
Scatter(
    plot4, a, b, pointer=Pointer.DIAMOND, pointer_color=(255, 50, 255), pointer_index=7
)

display.show()
