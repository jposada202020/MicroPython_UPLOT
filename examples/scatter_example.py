# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import gc
from random import choice
from machine import Pin, SPI
from ili9486 import ILI9486
from micropython_uplot.colors import create_color
from micropython_uplot.plot import PLOT
from micropython_uplot.utils import linspace
from micropython_uplot.scatter import Scatter

# Pin definition
pdc = Pin(8, Pin.OUT, value=0)
prst = Pin(15, Pin.OUT, value=1)
pcs = Pin(9, Pin.OUT, value=1)
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12), baudrate=30_000_000)
gc.collect()
display = ILI9486(spi, pcs, pdc, prst)

GREEN = create_color(display, 1, 0, 255, 0)
BLACK = create_color(display, 2, 0, 0, 0)

plot = PLOT(display, 50, 50, 200, 200, padding=1, box_color=(0, 0, 255))
plot.axs_params(axstype="box")
plot.tick_params(
    tickx_height=12, ticky_height=12, tickcolor=(100, 100, 100), tickgrid=True
)

a = list(linspace(1, 100, 100))
b = [choice(a) for _ in a]
Scatter(plot, a, b, pointer="diamond")

display.show()
