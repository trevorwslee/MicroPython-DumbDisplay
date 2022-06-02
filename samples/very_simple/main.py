

# assume a _my_secret.py Python sript containing
#   WIFI_SSID="SSID"
#   WIFI_PWD="PASSWORD"
from _my_secret import *

from dumbdisplay.core import *
from dumbdisplay.io_wifi import *
from dumbdisplay.layer_ledgrid import *


import time


dd = DumbDisplay(io4Wifi(WIFI_SSID, WIFI_PWD))
l = LayerLedGrid(dd, 2, 1)
l.offColor("green")
l.turnOn()
for _ in range(10):
    time.sleep(1)
    l.toggle(0, 0)
    l.toggle(1, 0)
dd.writeComment("DONE")    
    
