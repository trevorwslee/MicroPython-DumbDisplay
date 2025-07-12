from dumbdisplay.core import *
from dumbdisplay.layer_ledgrid import *
import time


# # create DumbDisplay
# if DumbDisplay.runningWithMicropython():
#     # connect using WIFI:
#     # assume a _my_secret.py Python script containing
#     #   WIFI_SSID="SSID"
#     #   WIFI_PWD="PASSWORD"
#     from _my_secret import *
#     from dumbdisplay.io_wifi import *
#     dd = DumbDisplay(io4Wifi(WIFI_SSID, WIFI_PWD))
#     print("***** WIFI *****")
# else:
#     # connect using Inet (Python Internet connection)
#     from dumbdisplay.io_inet import *
#     dd = DumbDisplay(io4Inet())


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

