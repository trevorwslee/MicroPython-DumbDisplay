#
# moved to dumbdisplay.examples.passive_blink
#


from dumbdisplay.core import *
from dumbdisplay.layer_ledgrid import *
import time


# create DumbDisplay
if DumbDisplay.runningWithMicropython():
    try:
        # connect using WIFI:
        # assume a _my_secret.py Python script containing
        #   WIFI_SSID="SSID"
        #   WIFI_PWD="PASSWORD"
        from _my_secret import *
        from dumbdisplay.io_wifi import *
        dd = DumbDisplay(io4Wifi(WIFI_SSID, WIFI_PWD))
        print("***** WIFI *****")
    except:
        # assume BLUETOOTH
        from dumbdisplay.io_uart import *
        dd = DumbDisplay(io4Uart(id=1, baudrate=115200, rx=9, tx=8))
        print("***** BLUETOOTH *****")
else:
    # connect using Inet (Python Internet connection)
    from dumbdisplay.io_inet import *
    dd = DumbDisplay(io4Inet())
    
try:
    import sys
    from machine import Pin
    try:
        led = Pin("LED", Pin.OUT)
        print("*** LED=LED")
    except:
        led = None
    if led is None:    
        if sys.implementation._machine.startswith("ESP32C3"):
            # assume MINI ESP32C3
            led = Pin(8, Pin.OUT)
            print("*** LED=8")
        else:    
            # assume ESP32
            led = Pin(2, Pin.OUT)
            print("*** LED=2")
except:
    led = None

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
        if led is not None:
            if led.value():
                led.off()
            else:
                led.on()
        last_ms = now_ms

