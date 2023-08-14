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
from micropython_uplot.scatter import Scatter, Pointer

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


a = list(linspace(10, 200, 50))
z = [2, 3, 4, 5, 6]
radi = [choice(z) for _ in a]
b = [choice(a) for _ in a]
Scatter(
    plot,
    a,
    b,
    rangex=[0, 210],
    rangey=[0, 210],
    radius=radi,
    pointer_color=(255, 255, 0),
)
a = list(linspace(50, 170, 50))
radi = [choice(z) for _ in a]
b = [choice(a) for _ in a]
Scatter(
    plot,
    a,
    b,
    rangex=[0, 210],
    rangey=[0, 210],
    radius=radi,
    pointer_color=(255, 69, 69),
)
a = list(linspace(50, 100, 25))
z = [
    4,
    5,
    6,
]
radi = [choice(z) for _ in a]
b = [int(choice(a) / 1.2) for _ in a]
Scatter(
    plot,
    a,
    b,
    rangex=[0, 210],
    rangey=[0, 210],
    pointer=Pointer.TRIANGLE,
    pointer_color=(34, 98, 129),
)

display.show()
plot.savingppm("newfile.ppm")
