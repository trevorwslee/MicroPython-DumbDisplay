# DumbDisplay MicroPython Library (v0.4.0)

DumbDisplay MicroPython Library -- workable with Python 3 -- is a port of the [DumbDisplay Arduino Library](https://github.com/trevorwslee/Arduino-DumbDisplay)
to Micro-Python / Python 3 for the [DumbDisplay Android app](https://play.google.com/store/apps/details?id=nobody.trevorlee.dumbdisplay)

For a video introduction, please watch the YouTube video: [Introducing DumbDisplay MicroPython Library -- 
with ESP32, Raspberry Pi Pico, and Raspberry Pi Zero](https://www.youtube.com/watch?v=KVU26FyXs5M)

Although the porting is not complete, nevertheless, a large portion of DumbDisplay functionalities have been ported.
Hopefully, this should already be helpful for friends that develop programs for microcontroller boards in Micro-Python.

As hinted previously,  even it is originally targeted for MicroPython, it should be useful with regular Python 3, like in Raspberry Pi environment
or even with desktop / laptop.


Enjoy

- [DumbDisplay MicroPython Library (v0.4.0)](#dumbdisplay-micropython-library-v040)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Selected Demos](#selected-demos)
- [Thank You!](#thank-you)
- [License](#license)
- [Change History](#change-history)


# Installation

For Micro-Python, please refer to the [above-mentioned YouTube video](https://www.youtube.com/watch?v=KVU26FyXs5M)
for examples of using DumbDisplay MicroPython Library for microcontroller boards programming.

If your targeted is desktop / laptop, you can install the library by cloning the repository:
```
pip install git+https://github.com/trevorwslee/MicroPython-DumbDisplay
```

If you would like to try out the development version (for desktop / laptop), you can install the development version like:
```
pip install --upgrade --force-reinstall git+https://github.com/trevorwslee/MicroPython-DumbDisplay@develop
```


# Getting Started

The basic script setup is:
1. import core, for creating `DumbDisplay` object
2. import IO mechanism, for creating IO object
3. import layers, for creating layer objects

For example
```
from dumbdisplay.core import *
from dumbdisplay.io_inet import *
from dumbdisplay.layer_ledgrid import *
dd = DumbDisplay(io4Inet())
l = LayerLedGrid(dd)
l.turnOn()
```


A "very simple" sample that makes use of WiFi can be like
```
from dumbdisplay.core import *
from dumbdisplay.io_wifi import *
from dumbdisplay.layer_ledgrid import *
import time
dd = DumbDisplay(io4Wifi("ssid", "password"))
l = LayerLedGrid(dd, 2, 1)
l.offColor("green")
l.turnOn()
for _ in range(10):
    time.sleep(1)
    l.toggle(0, 0)
    l.toggle(1, 0)
dd.writeComment("DONE")    
```


A simple sample that polls for feedbacks, can be like
```
from dumbdisplay.core import *
from dumbdisplay.io_inet import *
from dumbdisplay.layer_ledgrid import *
dd = DumbDisplay(io4Inet())
l = LayerLedGrid(dd, 20, 20)
l.enableFeedback("fa")
l.offColor(RGB_COLOR(0xcc, 0xcc, 0xcc))
while True:
    feedback = l.getFeedback()
    if feedback is not None:
        print("l FB: {}: {},{}".format(feedback.type, feedback.x, feedback.y))
        l.toggle(feedback.x, feedback.y)
```

A more complete simple sample that also shows "auto pin" as well, can be like
```
from dumbdisplay.core import *
from dumbdisplay.io_inet import *
from dumbdisplay.layer_lcd import *
from dumbdisplay.layer_graphical import *

_last_x = -1
_color = "red"
def feedback_handler(layer, type, x, y):
    global _last_x, _last_y, _color
    if layer == l:
        if _last_x != -1:
            l.drawLine(_last_x, _last_y, x, y, _color)
        _last_x = x
        _last_y = y
    else:    
        if layer == l_r:
            _color = "red"
        elif layer == l_g:
            _color = "green"
        elif layer == l_b:
            _color = "blue"            
        _last_x = -1   


dd = DumbDisplay(io4Inet())
l_r = LayerLcd(dd)
l_g = LayerLcd(dd)
l_b = LayerLcd(dd)
l = LayerGraphical(dd, 150, 100)
l_r.backgroundColor("red")
l_g.backgroundColor("green")
l_b.backgroundColor("blue")
l.backgroundColor("white")
l.border(3, "black")
l_r.enableFeedback("f", feedback_handler=feedback_handler)
l_g.enableFeedback("f", feedback_handler=feedback_handler)
l_b.enableFeedback("f", feedback_handler=feedback_handler)
l.enableFeedback("fs:rpt50", feedback_handler=feedback_handler)
AutoPin('V', AutoPin('H', l_r, l_g, l_b), l).pin(dd)
while True:
    dd.sleep(1)
```

Notes:
* If seeing ESP32 brownout detection issue, try 
    ```
    import machine
    machine.reset_cause()
    ```
* If DumbDisplay Android app fails to make connection to desktop / laptop, check your desktop firewall settings; try switching desktop WIFI to use 2.4 GHz.


# Selected Demos

Here is a few Raspberry Pi Pico PIO demos that might interested you

|[Respberry Pi Pico W Generating Tones With Programmable I/O (PIO) Using MicroPython](https://www.instructables.com/Respberry-Pi-Pico-W-Generating-Tones-With-Programm/)|[Respberry Pi Pico W NeoPixels Experiments With Programmable I/O (PIO) Using MicroPython](https://www.instructables.com/Respberry-Pi-Pico-W-NeoPixels-Experiments-With-Pro/)|
|--|--|
|![](screenshots/u_melody_dd.jpg)|![](screenshots/u_neopixeldd_dd.jpg)|



# Thank You!

Greeting from the author Trevor Lee:

> Peace be with you!
> May God bless you!
> Jesus loves you!
> Amazing Grace!


# License

MIT


# Change History

v0.4.0
- ported "level options" for LayerGraphical 
- ported LayerSelection
- bug fixes

v0.3.1
- ported LayerJoystick

v0.3.0
- checked Raspberry Pi Pico W WIFI support
- ported more options from Arduino DumbDisplay library
- bug fixes

v0.2.1
- ported LayerPlotter
- ported "layer margin"
- bug fixes


