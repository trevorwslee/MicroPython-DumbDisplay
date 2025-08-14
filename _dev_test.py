import random
from dumbdisplay.dumbdisplay import DumbDisplay
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
    l = LayerTurtleTracked(dd, 2000, 2000)
    l.backgroundColor("ivory")
    l.border(3, "blue")
    if True:
        sync = True
        distance = 1
        angle = 10
        for i in range(0, 180):
            l.penColor("red")
            l.penSize(20)
            l.forward(distance)
            l.rightTurn(angle)
            distance += 1
            coor = l.pos(sync=sync)
            if True:
                l.goTo(0, 0, with_pen=False)
                l.penColor("blue")
                l.penSize(10)
                l.circle(15 * i, centered=True)
            l.goTo(coor[0], coor[1], with_pen=False)
            print(f"* LOOP[{i}] turtle pos: {coor}")
            if not sync:
                dd.sleep(0.1)
    else:
        l.forward(100)
        coor = l.pos()
        print(f"* INIT turtle pos: {coor}")
        l.forward(100)
        coor = l.pos()
        print(f"* INIT 2 turtle pos: {coor}")
    while True:
        coor = l.pos()
        print(f"* turtle pos: {coor}")
        dd.sleep(2)

def test_passive_turtleTracked(sync: bool = True):
    from dumbdisplay.layer_turtle import LayerTurtleTracked
    def _setup(dd: DumbDisplay) -> LayerTurtleTracked:
        l = LayerTurtleTracked(dd, 2000, 2000)
        l.backgroundColor("ivory")
        l.border(3, "blue")
        return l
    def _loop(l: LayerTurtleTracked, i: int, distance: int):
        if i > 300:
            coor = l.pos(sync=sync)
            print(f"* ENDED turtle pos: {coor}")
            l.dd.sleep(2)
            return
        l.penColor("red")
        l.penSize(20)
        l.forward(distance)
        l.rightTurn(10)
        if True:
            r = 50 + int(random.random() * 30)
            r2 = r + 10 + int(random.random() * 20)
            a = int(random.random() * 45)
            a2 = a + 10 + int(random.random() * 45)
            centered = random.random() < 0.5
            l.penColor("green")
            l.penSize(10)
            shape = i % 7
            if shape == 0:
                l.rectangle(r, r2, centered=centered)
            elif shape == 1:
                l.centeredPolygon(r, 5, inside=centered)
            elif shape == 2:
                l.polygon(r, 5)
            elif shape == 3:
                l.arc(r, r2, a, a2, centered=centered)
            elif shape == 4:
                l.circle(r, centered=centered)
            elif shape == 5:
                l.isoscelesTriangle(r, a)
            else:
                l.dot(r, color="darkblue")
        coor = l.pos(sync=sync)
        if i % 2 == 0:
            l.goTo(0, 0, with_pen=False)
            l.penColor("blue")
            l.penSize(5)
            r = 5 * i
            l.circle(r, centered=True)
            l.goTo(coor[0], coor[1], with_pen=False)
        print(f"* LOOP[{i}] turtle pos: {coor}")
        # if not sync:
        #     l.dd.sleep(0.2)
    dd = create_example_wifi_dd()
    distance = 1
    i = 0
    l: LayerTurtleTracked = None
    while True:
        (connected, reconnecting) = dd.connectPassive()
        if connected:
            if l is None:
                l = _setup(dd)
                distance = 1
                i = 0
            else:
              if reconnecting:
                dd.masterReset()
                l = None
              else:
                _loop(l, i=i, distance=distance)
                distance = distance + 1
                i = i + 1




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

    test_passive_turtleTracked(sync=True)

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
