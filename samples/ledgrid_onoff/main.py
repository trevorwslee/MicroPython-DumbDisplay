
from dumbdisplay.core import *
from dumbdisplay.layer_ledgrid import *


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


l = LayerLedGrid(dd, 20, 20)
l.enableFeedback("fa")
l.offColor(RGB_COLOR(0xcc, 0xcc, 0xcc))
while True:
    feedback = l.getFeedback()
    if feedback is not None:
        print("l FB: {}: {},{}".format(feedback.type, feedback.x, feedback.y))
        l.toggle(feedback.x, feedback.y)
