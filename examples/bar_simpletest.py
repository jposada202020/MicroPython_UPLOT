# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import gc
from machine import Pin, SPI
from ili9486 import ILI9486
from micropython_uplot.plot import PLOT
from micropython_uplot.bar import Bar


# Pin definition
pdc = Pin(8, Pin.OUT, value=0)
prst = Pin(15, Pin.OUT, value=1)
pcs = Pin(9, Pin.OUT, value=1)
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12), baudrate=30_000_000)
gc.collect()
display = ILI9486(spi, pcs, pdc, prst)


my_plot = PLOT(display, 10, 10, 250, 250, padding=1, box_color=(255, 255, 255))
my_plot.axs_params(axstype="box")

# Setting up tick parameters
a = ["a", "b", "c", "d"]
b = [3, 5, 1, 7]
colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
]


Bar(my_plot, a, b, (255, 255, 255), True, bar_space=20, xstart=8)
# Uncomment the following line to use customize colors
# Bar(my_plot, a, b, (255, 255, 255), True, bar_space=16, xstart=5, color_palette=colors)

# Plotting and showing the plot
display.show()
my_plot._savingppm("bar.ppm")
