# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import random
import gc
from machine import Pin, SPI
from ili9486 import ILI9486
from micropython_uplot.plot import PLOT
from micropython_uplot.logging import Logging

# Pin definition
pdc = Pin(8, Pin.OUT, value=0)
prst = Pin(15, Pin.OUT, value=1)
pcs = Pin(9, Pin.OUT, value=1)
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12), baudrate=30_000_000)
gc.collect()
display = ILI9486(spi, pcs, pdc, prst)

my_plot = PLOT(display, 5, 5, 300, 250, padding=25, box_color=(255, 255, 255))
my_plot.tick_params(
    tickx_height=4,
    ticky_height=4,
    show_ticks=True,
    tickcolor=(255, 125, 125),
    showtext=True,
)

# Creating the x and y data
x = [
    10,
    20,
    30,
    40,
    50,
    60,
    70,
    80,
    90,
    100,
    110,
    120,
    130,
    140,
    150,
    160,
    170,
    180,
    190,
]
y = [26, 22, 24, 30, 28, 35, 26, 25, 24, 23, 20, 27, 26, 33, 24, 23, 19, 27, 26]

# Creating the random numbers
random_numbers = [19, 22, 35, 33, 24, 26, 28, 37]


dist = 1

# Creating the loggraph
my_loggraph = Logging(
    my_plot,
    x[0:dist],
    y[0:dist],
    rangex=[0, 210],
    rangey=[0, 110],
    line_color=(0, 255, 0),
    ticksx=[25, 50, 75, 100, 125, 150, 175, 200],
    ticksy=[25, 50, 75, 100],
)

display.show()

# Showing the loggraph
for _ in range(20):
    if dist > len(x):
        y.pop(0)
        y.append(random.choice(random_numbers))

    my_loggraph.draw_points(my_plot, x[0:dist], y[0:dist])
    display.show()
    dist += 1
    time.sleep(0.5)
