from dumbdisplay.core import *
from dumbdisplay.layer_ledgrid import *
import time

# create DumbDisplay
if DumbDisplay.runningWithMicropython():
    # connect using WIFI:
    # assume a _my_secret.py Python script containing
    #   WIFI_SSID="SSID"
    #   WIFI_PWD="PASSWORD"
    from _my_secret import *
    from dumbdisplay.io_wifi import *
    dd = DumbDisplay(io4Wifi(WIFI_SSID, WIFI_PWD))
else:
    # connect using Inet (Python Internet connection)
    from dumbdisplay.io_inet import *
    dd = DumbDisplay(io4Inet())

l: LayerLedGrid = None
last_ms = time.ticks_ms()
is_on = False
while True:
    (connected, reconnecting) = dd.connectPassive()
    if connected:
        if l is None:
            l = LayerLedGrid(dd)
            l.offColor("green")
            l.turnOn()
        elif reconnecting:
            dd.masterReset()
            l = None
    now_ms = time.ticks_ms()
    diff_ms = now_ms - last_ms
    if diff_ms >= 1000:
        if l is not None:
            l.toggle()
        last_ms = now_ms

