import random
import time
import math


from dumbdisplay.core import *
from dumbdisplay_examples.utils import create_example_wifi_dd


def run_debug():
    #import projects.testing.main as test
    import experiments.testing.main as test
    test.runDebug()

def run_doodle():
    import samples.doodle.main

def run_graphical():
    import samples.graphical.main

def run_melody():
    import samples.melody.main


def test_very_simple():
    #import time
    from dumbdisplay.layer_ledgrid import LayerLedGrid
    dd = DumbDisplay()  # default io is io4Inet()
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
    dd = DumbDisplay()  # default io is io4Inet()
    l = LayerPlotter(dd, 300, 100)
    l.label("X", sin="Sin")
    for x in range(1000):
        sin = math.sin(x)
        l.set(x, sin=sin)
        time.sleep(0.5)


def test_margin():
    from dumbdisplay.layer_ledgrid import LayerLedGrid
    dd = DumbDisplay()  # default io is io4Inet()
    l = LayerLedGrid(dd)
    dd.backgroundColor("yellow")
    l.backgroundColor("pink")
    l.turnOn()
    l.padding(0.1, 0.2, 0.3, 0.4)
    l.border(0.2, "green", "round", 0.1)
    l.margin(0.4, 0.3, 0.2, 0.1)
    while True:
        print("... ", end="")
        dd.timeslice()
        print("...")
        if dd.isReconnecting():
            break # since haven't setup for reconnection (like with recordLayerSetupCommands) ... may as well break out of the loop
    print("... ASSUME disconnected")


def run_passive_blink_app():
    from dumbdisplay_examples.passive_blink.passive_blink_app import PassiveBlinkApp
    print(f"*** PassiveBlinkApp ***")
    app = PassiveBlinkApp(create_example_wifi_dd())
    app.run()


def run_sliding_puzzle_app():
    from dumbdisplay_examples.sliding_puzzle.sliding_puzzle_app import SlidingPuzzleApp
    print(f"*** SlidingPuzzleApp ***")
    suggest_move_from_dir_func = lambda board_manager: random.randint(0, 3)
    app = SlidingPuzzleApp(create_example_wifi_dd(), suggest_move_from_dir_func=suggest_move_from_dir_func)
    app.run()

def run_mnist_app():
    from dumbdisplay_examples.mnist.mnist_app import MnistApp
    print(f"*** MnistApp ***")
    inference_func = lambda board_manager: random.randint(0, 10)
    app = MnistApp(create_example_wifi_dd(), inference_func=inference_func)
    app.run()



def test_read_readme():
    from pathlib import Path
    this_directory = Path(__file__).parent
    long_description = (this_directory / "README.md").read_text()
    print(long_description)

def test_find_packages():
    from setuptools.config.expand import find_packages
    packages = find_packages(include=["dumbdisplay*"])
    print(f"Found packages: {packages}")



if __name__ == "__main__":
    #run_passive_blink_app()
    #run_sliding_puzzle_app()
    run_mnist_app()

    #run_debug()
    #run_doodle()
    #run_graphical()
    #run_melody()

    #test_margin()
    #test_very_simple()
    #test_plotter()

    #test_read_readme()
    #test_find_packages()
