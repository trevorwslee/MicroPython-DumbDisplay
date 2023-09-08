
from dumbdisplay.core import *
from dumbdisplay.layer_lcd import *
from dumbdisplay.layer_graphical import *


# initialize some global variables
_last_x = -1
_color = "red"

# feedback handler
def feedback_handler(layer, type, x, y):
    global _last_x, _last_y, _color
    if layer == l:
        if _last_x != -1:
            l.drawLine(_last_x, _last_y, x, y, _color)
        _last_x = x
        _last_y = y
    else:    
        if layer == l_r:
            _color = "red"
        elif layer == l_g:
            _color = "green"
        elif layer == l_b:
            _color = "blue"            
        _last_x = -1   


# create DumbDisplay connected using Inet (Python Internet connection)
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

# create 3 LCD layer as 3 tabs for changing color
l_r = LayerLcd(dd)
l_g = LayerLcd(dd)
l_b = LayerLcd(dd)

# set the background color of the 3 tabs
l_r.backgroundColor("red")
l_g.backgroundColor("green")
l_b.backgroundColor("blue")


# create the main graphical [LCD] layer
l = LayerGraphical(dd, 150, 100)

# set the background color as well as border for the graphical layer
l.backgroundColor("white")
l.border(3, "black")

# enable feedback for the 3 tabs
l_r.enableFeedback("f", feedback_handler)
l_g.enableFeedback("f", feedback_handler)
l_b.enableFeedback("f", feedback_handler)

#enable feedback for the core graphical layer, note that it is set to "auto repeat" every 50 milli-seconds
l.enableFeedback("fs:rpt50", feedback_handler)

# "auto pin" the different layers
AutoPin('V', AutoPin('H', l_r, l_g, l_b), l).pin(dd)

# the main loop does nothing, but uses DumbDisplay's delay, so that DumbDisplay has a chnace to do it's work
while True:
    dd.delay(1)



