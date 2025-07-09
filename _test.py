import time
import math
from dumbdisplay.core import *
from dumbdisplay.io_inet import *
#from dumbdisplay.layers import *


def run_debug():
    #import projects.testing.main as test
    import experiments.testing.main as test
    test.runDebug()

def run_passive_blink():
    import experiments.passive.passive_blink.main

def run_graphical():
    import samples.graphical.main

def very_simple():
    #import time
    from dumbdisplay.layer_ledgrid import LayerLedGrid
    dd = DumbDisplay(io4Inet())
    l = LayerLedGrid(dd, 2, 1)
    l.offColor("green")
    l.turnOn()
    for _ in range(1000):
        time.sleep(1)
        l.toggle(0, 0)
        l.toggle(1, 0)
    dd.writeComment("DONE")    


def test_plotter():
    from dumbdisplay.layer_plotter import LayerPlotter
    dd = DumbDisplay(io4Inet())
    l = LayerPlotter(dd, 300, 100)
    l.label("X", sin="Sin")
    for x in range(1000):
        sin = math.sin(x)
        l.set(x, sin=sin)
        time.sleep(0.5)


def test_margin():
    from dumbdisplay.layer_ledgrid import LayerLedGrid
    dd = DumbDisplay(io4Inet())
    l = LayerLedGrid(dd)
    dd.backgroundColor("yellow")
    l.backgroundColor("pink")
    l.turnOn()
    l.padding(0.1, 0.2, 0.3, 0.4)
    l.border(0.2, "green", "round", 0.1)
    l.margin(0.4, 0.3, 0.2, 0.1)
    time.sleep(10000)



if __name__ == "__main__":
    #run_debug()

    run_passive_blink()
    #run_graphical()
    #very_simple()
    #test_margin()
    #test_plotter()
