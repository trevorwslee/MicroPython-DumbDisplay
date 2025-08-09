# DumbDisplay MicroPython Library (v0.5.0)

DumbDisplay MicroPython Library -- workable with Python 3 -- is a port of the [DumbDisplay Arduino Library](https://github.com/trevorwslee/Arduino-DumbDisplay)
to Micro-Python / Python 3 for the [DumbDisplay Android app](https://play.google.com/store/apps/details?id=nobody.trevorlee.dumbdisplay)

For a video introduction, please watch the YouTube video: [Introducing DumbDisplay MicroPython Library -- 
with ESP32, Raspberry Pi Pico, and Raspberry Pi Zero](https://www.youtube.com/watch?v=KVU26FyXs5M)

Although the porting is work in progress, nevertheless, a large portion of DumbDisplay functionalities have been ported.
Hopefully, this should already be helpful for friends that develop programs for microcontroller boards in Micro-Python.

As hinted previously, even it is originally targeted for MicroPython, it should be useful with regular Python 3, like in Raspberry Pi environment
or even with desktop / laptop.
As a result, it can be an alternative way to prototype Android app driven remotely with Python 3 from desktop / laptop.


Enjoyz

- [DumbDisplay MicroPython Library (v0.5.0)](#dumbdisplay-micropython-library-v050)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Selected Demos](#selected-demos)
- [Thank You!](#thank-you)
- [License](#license)
- [Change History](#change-history)


# Installation

For Micro-Python, please refer to the [above-mentioned YouTube video](https://www.youtube.com/watch?v=KVU26FyXs5M)
for examples of using DumbDisplay MicroPython Library for microcontroller programming.

If your targeted is desktop / laptop, you can install the package like:
```
pip install git+https://github.com/trevorwslee/MicroPython-DumbDisplay
```

>
> If you would like to try out the development version (for desktop / laptop), you can install the development version like:
> ```
> pip install --upgrade --force-reinstall git+https://github.com/trevorwslee/MicroPython-DumbDisplay@develop
> ```
> 
> To switch back after trying the development version, run
> ```
> pip install --upgrade --force-reinstall git+https://github.com/trevorwslee/MicroPython-DumbDisplay
> ```
>


# Getting Started

The basic Python script setup is:
1. import core, for creating `DumbDisplay` object
   <br>e.g.
   ```
   from dumbdisplay.core import *
   dd = DumbDisplay()
   ```
   - you can import the "core" components with ```from dumbdisplay.core import *```
   - or you can choose to import "all" components (including layers to be mentioned later) with ```from dumbdisplay.full import *```
2. import IO mechanism, for creating IO object [to pass to DumbDisplay object], like
   - `io4Inet` (the default) -- Python networking support (not available for Micro-Python)
   - `io4Wifi` -- Micro-Python WiFi support (for Raspberry Pi Pico W, ESP32, etc.)
   <br>e.g.
   ```
   from dumbdisplay.core import *
   from dumbdisplay.io_inet import *
   dd = DumbDisplay(io4Wifi("ssid", "password"))
   ```
3. import layers, for creating layer objects [passing DumbDisplay object to them]
   - `LayerLedGrid` -- a single LED, or a grid of multiple LEDs (**n** columns by **m** rows)
     <br>e.g.
     ```
     from dumbdisplay.core import *
     from dumbdisplay.layer_ledgrid import *
     dd = DumbDisplay()
     l = LayerLedGrid(dd)
     ```
     |[`demo_LayerLedGrid()` in `dd_demo.py`](dd_demo.py)|
     |--|
     |<img style="width: 200px; height: 200px;" src="screenshots/layer_ledgrid_2x2.png"></img>|

   - `LayerLcd` -- a TEXT based LCD with configurable number of lines of configurable number of characters
     <br>e.g.
     ```
     from dumbdisplay.core import *
     from dumbdisplay.layer_lcd import *
     dd = DumbDisplay()
     l = LayerLcd(dd)
     ```
     |[`demo_LayerLcd()` in `dd_demo.py`](dd_demo.py)|
     |--|
     |<img style="width: 200px; height: 200px;" src="screenshots/layer_lcd.png"></img>|

   - `LayerGraphical` -- a graphical LCD that you can draw to, with common drawing operations
     <br>e.g.
     ```
     from dumbdisplay.core import *
     from dumbdisplay.layer_graphical import *
     dd = DumbDisplay()
     l = LayerGraphical(dd)
     ```
     |[`demo_LayerGraphical()` in `dd_demo.py`](dd_demo.py)|
     |--|
     |<img style="width: 200px; height: 200px;" src="screenshots/layer_graphical.png"></img>|

   - `LayerSelection` -- a group / grid of TEXT based LCD mostly for showing selection choices
     <br>e.g.
     ```
     from dumbdisplay.core import *
     from dumbdisplay.layer_selection import *
     dd = DumbDisplay()
     l = LayerSelection(dd)
     ```
     |[`demo_LayerSelection()` in `dd_demo.py`](dd_demo.py)|
     |--|
     |<img style="width: 200px; height: 200px;" src="screenshots/layer_selection_1x3.png"></img>|

   - `Layer7SegmentRow` -- a single 7-segment digit, or a row of **n** 7-segments digits
     <br>e.g.
     ```
     from dumbdisplay.core import *
     from dumbdisplay.layer_7segrow import *
     dd = DumbDisplay()
     l = Layer7SegmentRow(dd)
     ```
     |[`demo_Layer7SegmentRow()` in `dd_demo.py`](dd_demo.py)|
     |--|
     |<img style="width: 200px; height: 200px;" src="screenshots/layer_7segment_3d.png"></img>|

   - `LayerPlotter` -- a "plotter"
     <br>e.g.
     ```
     from dumbdisplay.core import *
     from dumbdisplay.layer_plotter import *
     dd = DumbDisplay()
     l = LayerPlotter(dd)
     ```
     |[`demo_LayerPlotter()` in `dd_demo.py`](dd_demo.py)|
     |--|
     |<img style="width: 200px; height: 200px;" src="screenshots/layer_plotter.png"></img>|

4. if you have multiple layers, you can "auto pin" them together
     <br>e.g.
     ```
     AutoPin('V', AutoPin('H', l_ledgrid, l_lcd), AutoPin('H', l_selection, l_7segmentrow), l_graphical).pin(dd)
     ```
     |[`demo_AutoPin()` in `dd_demo.py`](dd_demo.py)|
     |--|
     |<img style="width: 300px; height: 300px;" src="screenshots/autopin_layers.png"></img>|
     




For example (using Python networking support with `io4Inet` as `io` for the DumbDisplay object)
```
from dumbdisplay.core import *
from dumbdisplay.io_inet import *
from dumbdisplay.layer_ledgrid import *
dd = DumbDisplay(io4Inet())  # actually, default io is io4Inet()
l = LayerLedGrid(dd)
l.turnOn()
```


A simple sample that explicitly makes use of WiFi `io4Wifi` as `io` for the DumbDisplay object, can be like
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
dd = DumbDisplay()  # default io is io4Inet()
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


dd = DumbDisplay()  # default io is io4Inet()
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
    dd.timeslice()
```

Notes:
* If seeing ESP32 brownout detection issue, try 
    ```
    import machine
    machine.reset_cause()
    ```
* If DumbDisplay Android app fails to make connection to desktop / laptop, check your desktop firewall settings; try switching desktop WIFI to use 2.4 GHz.


# Selected Demos

Here is a few Raspberry Pi Pico PIO demos that might interest you

|[Respberry Pi Pico W Generating Tones With Programmable I/O (PIO) Using MicroPython](https://www.instructables.com/Respberry-Pi-Pico-W-Generating-Tones-With-Programm/)|[Respberry Pi Pico W NeoPixels Experiments With Programmable I/O (PIO) Using MicroPython](https://www.instructables.com/Respberry-Pi-Pico-W-NeoPixels-Experiments-With-Pro/)|
|--|--|
|![](screenshots/u_melody_dd.jpg)|![](screenshots/u_neopixeldd_dd.jpg)|


[`PyTorchIntroductoryExperiments`](https://github.com/trevorwslee/PyTorchIntroductoryExperiments) shows two regular Python 3 demos that might interest you

|||
|--|--|
|![](screenshots/dd-mnist.jpg)|![](screenshots/dd-sliding-puzzle.jpg)|



# Thank You!

Greeting from the author Trevor Lee:

> Peace be with you!
> May God bless you!
> Jesus loves you!
> Amazing Grace!


# License

MIT


# Change History

v0.5.0
- ported "level options" for LayerGraphical 
- ported LayerSelection
- added dumbdisplay_examples package
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


