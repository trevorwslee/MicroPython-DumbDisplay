import machine
from neopixel import NeoPixel

import time


np = NeoPixel(machine.Pin(22), 4)


rgb = 0
i = 0
while True:
    if rgb == 0:
        c = (255, 0, 0)
    elif rgb == 1:
        c = (0, 255, 0)
    elif rgb == 2:
        c = (0, 0, 255)
    np[i] = c
    np.write()
    time.sleep(1)
    np[i] = (0, 0, 0)
    np.write()
    rgb = (rgb + 1) % 3
    i = (i + 1) % 4