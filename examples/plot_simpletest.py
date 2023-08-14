# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import gc
from machine import Pin, SPI
from ili9486 import ILI9486
from micropython_uplot.plot import PLOT


# Pin definition
pdc = Pin(8, Pin.OUT, value=0)
prst = Pin(15, Pin.OUT, value=1)
pcs = Pin(9, Pin.OUT, value=1)
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12), baudrate=30_000_000)
gc.collect()
display = ILI9486(spi, pcs, pdc, prst)


my_plot = PLOT(display, 50, 50, 200, 200, padding=25, box_color=(0, 0, 255))
my_plot.axs_params(axstype="box")

x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220]
my_plot.tick_params(show_ticks=True, tickgrid=True, showtext=True)
my_plot._draw_ticks(x, y)


display.show()

# my_plot.savingppm()
