import random
import time
import math


from dumbdisplay_examples.utils import create_example_wifi_dd



def run_debug():
    import experiments.testing.main as test
    test.runDebug()

def run_debugBlepriority(ble_name: str):
    import experiments.testing.main as test
    test.runDebugBlePriority(ble_name)

def run_doodle():
    import samples.doodle.main

def run_graphical():
    import samples.graphical.main

def run_melody():
    import samples.melody.main


def test_turtleTracked():
    from dumbdisplay.layer_turtle import LayerTurtleTracked
    dd = create_example_wifi_dd()
    l = LayerTurtleTracked(dd, 100, 100)
    l.backgroundColor("ivory")
    l.border(3, "blue")
    l.forward(100)
    coor = l.pos()
    print(f"* INIT turtle pos: {coor}")
    while True:
        coor = l.pos()
        print(f"* turtle pos: {coor}")
        dd.sleep(2)


def test_margin():
    from dumbdisplay.layer_ledgrid import LayerLedGrid
    dd = create_example_wifi_dd()
    l = LayerLedGrid(dd)
    dd.backgroundColor("yellow")
    l.backgroundColor("pink")
    l.turnOn()
    l.padding(0.1, 0.2, 0.3, 0.4)
    l.border(0.2, "green", "round", 0.1)
    l.margin(0.4, 0.3, 0.2, 0.1)
    while True:
        print("... ", end="")
        dd.sleep(1)
        print("...")
        if dd.isReconnecting():
            break # since haven't setup for reconnection (like with recordLayerSetupCommands) ... may as well break out of the loop
    print("... ASSUME disconnected")


def run_passive_blink_app():
    from dumbdisplay_examples.passive_blink.passive_blink_app import PassiveBlinkApp
    print(f"*** PassiveBlinkApp ***")
    app = PassiveBlinkApp()
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

    test_turtleTracked()

    # run_debug()
    # run_doodle()
    # run_graphical()
    # run_melody()
    #
    # test_margin()
    #
    # run_debugBlepriority("MyBLEDevice")
    #
    # test_read_readme()
    # test_find_packages()
