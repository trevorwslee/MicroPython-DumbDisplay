from dumbdisplay.core import *
from dumbdisplay.layer_ledgrid import *
import time

if True:
    # assume a _my_secret.py Python script containing
    #   WIFI_SSID="SSID"
    #   WIFI_PWD="PASSWORD"
    from _my_secret import *
    from dumbdisplay.io_wifi import *
    dd = DumbDisplay(io4Wifi(WIFI_SSID, WIFI_PWD))
else:
    # can use UART ... say connected to HC-06
    from dumbdisplay.io_uart import *
    dd = DumbDisplay(io4Uart(id=1, baudrate=115200, rx=9, tx=8))

l = LayerLedGrid(dd, 2, 1)
l.offColor("green")
l.turnOn()
for _ in range(10):
    time.sleep(1)
    l.toggle(0, 0)
    l.toggle(1, 0)
dd.writeComment("DONE")    
    
