from dumbdisplay.core import *
from dumbdisplay.layer_ledgrid import *
import time


class PassiveBlinkApp():
    def __init__(self, dd: DumbDisplay):
        self.dd = dd
    def run(self):
        l: LayerLedGrid = None
        last_ms = time.ticks_ms()
        while True:
            (connected, reconnecting) = self.dd.connectPassive()
            if connected:
                if l is None:
                    l = LayerLedGrid(self.dd)
                    l.offColor("green")
                    l.turnOn()
                elif reconnecting:
                    self.dd.masterReset()
                    l = None
            now_ms = time.ticks_ms()
            diff_ms = now_ms - last_ms
            if diff_ms >= 1000:
                if l is not None:
                    l.toggle()
                last_ms = now_ms


if __name__ == "__main__":
    from dumbdisplay_examples.utils import create_example_wifi_dd
    app = PassiveBlinkApp(create_example_wifi_dd())
    app.run()
