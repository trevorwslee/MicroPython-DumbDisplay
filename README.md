# DumbDisplay MicroPython Library (v0.5.0)

DumbDisplay MicroPython Library -- workable with Python 3 -- is a port of the [DumbDisplay Arduino Library](https://github.com/trevorwslee/Arduino-DumbDisplay)
to MicroPython / Python 3 for the [DumbDisplay Android app](https://play.google.com/store/apps/details?id=nobody.trevorlee.dumbdisplay)

For a video introduction, please watch the YouTube video: [Introducing DumbDisplay MicroPython Library -- 
with ESP32, Raspberry Pi Pico, and Raspberry Pi Zero](https://www.youtube.com/watch?v=KVU26FyXs5M)

Although the porting is work in progress, nevertheless, most of the core of DumbDisplay functionalities have been ported.
Hopefully, this should already be helpful for friends that develop programs for microcontroller boards in Micro-Python.

As hinted previously, even it is originally targeted for MicroPython, it should be useful with regular Python 3, like in Raspberry Pi environment
or even with desktop / laptop.
Consequently, it might be an alternative way to prototype simple Android app driven remotely with Python 3 from desktop / laptop, say for displaying experiment result data and getting simple interaction with the user.


Enjoy

- [DumbDisplay MicroPython Library (v0.5.0)](#dumbdisplay-micropython-library-v050)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Selected Demos](#selected-demos)
- [Notes](#notes)
- [Thank You!](#thank-you)
- [License](#license)
- [Change History](#change-history)


# Installation

For MicroPython, please refer to the [above-mentioned YouTube video](https://www.youtube.com/watch?v=KVU26FyXs5M)
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
   - `io4Inet` (the default) -- Python networking support (not available for MicroPython)
   - `io4Wifi` -- MicroPython WiFi support (for Raspberry Pi Pico W, ESP32, etc.)
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
     |:--:|
     |<img style="width: 300px; height: 300px;" src="screenshots/layer_ledgrid_2x2.png"></img>|

   - `LayerLcd` -- a TEXT based LCD with configurable number of lines of configurable number of characters
     <br>e.g.
     ```
     from dumbdisplay.core import *
     from dumbdisplay.layer_lcd import *
     dd = DumbDisplay()
     l = LayerLcd(dd)
     ```
     |[`demo_LayerLcd()` in `dd_demo.py`](dd_demo.py)|
     |:--:|
     |<img style="width: 300px; height: 300px;" src="screenshots/layer_lcd.png"></img>|

   - `LayerGraphical` -- a graphical LCD that you can draw to, with common drawing operations
     <br>e.g.
     ```
     from dumbdisplay.core import *
     from dumbdisplay.layer_graphical import *
     dd = DumbDisplay()
     l = LayerGraphical(dd)
     ```
     |[`demo_LayerGraphical()` in `dd_demo.py`](dd_demo.py)|
     |:--:|
     |<img style="width: 300px; height: 300px;" src="screenshots/layer_graphical.png"></img>|

   - `LayerSelection` -- a group / grid of TEXT based LCD mostly for showing selection choices
     <br>e.g.
     ```
     from dumbdisplay.core import *
     from dumbdisplay.layer_selection import *
     dd = DumbDisplay()
     l = LayerSelection(dd)
     ```
     |[`demo_LayerSelection()` in `dd_demo.py`](dd_demo.py)|
     |:--:|
     |<img style="width: 300px; height: 300px;" src="screenshots/layer_selection_1x3.png"></img>|

   - `Layer7SegmentRow` -- a single 7-segment digit, or a row of **n** 7-segments digits
     <br>e.g.
     ```
     from dumbdisplay.core import *
     from dumbdisplay.layer_7segrow import *
     dd = DumbDisplay()
     l = Layer7SegmentRow(dd)
     ```
     |[`demo_Layer7SegmentRow()` in `dd_demo.py`](dd_demo.py)|
     |:--:|
     |<img style="width: 300px; height: 300px;" src="screenshots/layer_7segment_3d.png"></img>|

   - `LayerPlotter` -- a "plotter"
     <br>e.g.
     ```
     from dumbdisplay.core import *
     from dumbdisplay.layer_plotter import *
     dd = DumbDisplay()
     l = LayerPlotter(dd)
     ```
     |[`demo_LayerPlotter()` in `dd_demo.py`](dd_demo.py)|
     |:--:|
     |<img style="width: 300px; height: 300px;" src="screenshots/layer_plotter.png"></img>|

4. if you have multiple layers, you can "auto pin" them together; otherwise, multiple layers will be stacked on top of each other
     <br>e.g.
     ```
     AutoPin('V', AutoPin('H', l_ledgrid, l_lcd), AutoPin('H', l_selection, l_7segmentrow), l_graphical).pin(dd)
     ```
     |[`demo_AutoPin()` in `dd_demo.py`](dd_demo.py)|
     |:--:|
     |<img style="width: 400px; height: 400px;" src="screenshots/autopin_layers.png"></img>|
     

# Selected Demos

Here is a few Raspberry Pi Pico PIO demos that might interest you

|[Respberry Pi Pico W Generating Tones With Programmable I/O (PIO) Using MicroPython](https://www.instructables.com/Respberry-Pi-Pico-W-Generating-Tones-With-Programm/)|[Respberry Pi Pico W NeoPixels Experiments With Programmable I/O (PIO) Using MicroPython](https://www.instructables.com/Respberry-Pi-Pico-W-NeoPixels-Experiments-With-Pro/)|
|--|--|
|![](screenshots/u_melody_dd.jpg)|![](screenshots/u_neopixeldd_dd.jpg)|


[`PyTorchIntroductoryExperiments`](https://github.com/trevorwslee/PyTorchIntroductoryExperiments) shows two regular Python 3 demos that might interest you

|||
|--|--|
|![](screenshots/dd-mnist.jpg)|![](screenshots/dd-sliding-puzzle.jpg)|


# Notes
* If seeing ESP32 brownout detection issue, try 
    ```
    import machine
    machine.reset_cause()
    ```
* If DumbDisplay Android app fails to make connection to desktop / laptop, check your desktop firewall settings; try switching desktop WIFI to use 2.4 GHz.




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


