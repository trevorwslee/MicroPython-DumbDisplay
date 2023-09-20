from dumbdisplay.core import *
from dumbdisplay.layer_graphical import *
from dumbdisplay.layer_joystick import *

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

import time


color_layer = LayerGraphical(dd, 150, 101)
color_layer.border(5, "black", "round", 2)

r_slider_layer = LayerJoystick(dd, 255, "hori", 0.5)
r_slider_layer.border(3, "darkred", "round", 1)
r_slider_layer.colors("red", RGB_COLOR(0xff, 0x44, 0x44), "black", "darkgray")

g_slider_layer = LayerJoystick(dd, 255, "hori", 0.5)
g_slider_layer.border(3, "darkgreen", "round", 1)
g_slider_layer.colors("green", RGB_COLOR(0x44, 0xff, 0x44), "black", "darkgray")

b_slider_layer = LayerJoystick(dd, 255, "hori", 0.5)
b_slider_layer.border(3, "darkblue", "round", 1)
b_slider_layer.colors("blue", RGB_COLOR(0x44, 0x44, 0xff), "black", "darkgray")

AutoPin('V').pin(dd)

r = 0
g = 0
b = 0
color_layer.backgroundColor(RGB_COLOR(r, g, b))
while True:
    old_r = r
    old_g = g
    old_b = b
    fb: Feedback = r_slider_layer.getFeedback()
    if fb:
        r = fb.x
    fb: Feedback = g_slider_layer.getFeedback()
    if fb:
        g = fb.x
    fb: Feedback = b_slider_layer.getFeedback()
    if fb:
        b = fb.x
    if r != old_r or g != old_g or b != old_b:
        color_layer.backgroundColor(RGB_COLOR(r, g, b))
