
# assume MINIC3

NUM_PIXELS = 64
NEO_PIXELS_IN_PIN = 20
BRIGHTNESS = 3  # 0-255
LED_PIN = 8


try:
    from machine import Pin
    from neopixel import NeoPixel
    NP = NeoPixel(Pin(NEO_PIXELS_IN_PIN), NUM_PIXELS)
    LED = Pin(LED_PIN, Pin.OUT)
    print(f"*** LED={LED_PIN}")
except:
    NP = None
    LED = None


from dumbdisplay.core import *
from dumbdisplay.layer_lcd import *
from dumbdisplay.layer_graphical import *
from dumbdisplay.layer_joystick import *
from dumbdisplay.layer_7segrow import *
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


import time


led = None
auto_advance_tab = None

led_last_ms = time.ticks_ms()
auto_advance = None
auto_advance_last_ms = None
r = 0
g = 0
b = 0



while True:
    (connected, reconnecting) = dd.connectPassive()
    if connected:
        if led is None:
            led = LayerLedGrid(dd)
            led.offColor("yellow")
            led.enableFeedback("f")

            # crate a tab (LayerLcd) to control whether auto advance the pixel's color from the previous pixel to the next pixel
            auto_advance_tab = LayerLcd(dd, 12, 1)
            auto_advance_tab.writeCenteredLine("Auto Advance")
            auto_advance_tab.enableFeedback("fl")

            # crate a button (LayerLcd) to manually advance the pixel's color from the previous pixel to the next pixel
            advance_button = LayerLcd(dd, 3, 1)
            advance_button.border(1, "blue", "round")
            advance_button.writeCenteredLine(">>>")
            advance_button.enableFeedback("fl")

            # create 7-seg layer for the R HEX value
            r_7seg_layer = Layer7SegmentRow(dd,2)
            r_7seg_layer.border(10, "black")
            r_7seg_layer.backgroundColor("white", 50)

            # create 7-seg layer for the G HEX value
            g_7seg_layer = Layer7SegmentRow(dd,2)
            g_7seg_layer.border(10, "black")
            g_7seg_layer.backgroundColor("white", 50)

            # create 7-seg layer for the B HEX value
            b_7seg_layer = Layer7SegmentRow(dd,2)
            b_7seg_layer.border(10, "black")
            b_7seg_layer.backgroundColor("white", 50)

            # create a graphical layer (LayerGraphical) to show the color set using the following sliders
            color_layer = LayerGraphical(dd, 255, 255)
            color_layer.border(5, "black", "round", 2)
            color_layer.enableFeedback("fs:rpt50")

            # create R slider (LayerJoystick) for controlling R (0-255)
            r_slider_layer = LayerJoystick(dd, 255, "hori", 0.5)
            r_slider_layer.border(3, "darkred", "round", 1)
            r_slider_layer.colors("red", RGB_COLOR(0xff, 0x44, 0x44), "black", "darkgray")

            # create G slider (LayerJoystick) for controlling G (0-255)
            g_slider_layer = LayerJoystick(dd, 255, "hori", 0.5)
            g_slider_layer.border(3, "darkgreen", "round", 1)
            g_slider_layer.colors("green", RGB_COLOR(0x44, 0xff, 0x44), "black", "darkgray")

            # create B slider (LayerJoystick) for controlling B (0-255)
            b_slider_layer = LayerJoystick(dd, 255, "hori", 0.5)
            b_slider_layer.border(3, "darkblue", "round", 1)
            b_slider_layer.colors("blue", RGB_COLOR(0x44, 0x44, 0xff), "black", "darkgray")

            # auto "pin" the above layers
            AutoPin('V',
                    AutoPin('H', led, auto_advance_tab, advance_button),
                    AutoPin('S',
                            color_layer,
                            PaddedAutoPin('H', 25, 25, 25, 25, r_7seg_layer, g_7seg_layer, b_7seg_layer)),
                    r_slider_layer,
                    g_slider_layer,
                    b_slider_layer).pin(dd)

            r_7seg_layer.showHexNumber(r)
            g_7seg_layer.showHexNumber(g)
            b_7seg_layer.showHexNumber(b)
            color_layer.backgroundColor(RGB_COLOR(r, g, b))
            r_slider_layer.moveToPos(r, 0)
            g_slider_layer.moveToPos(g, 0)
            b_slider_layer.moveToPos(b, 0)

            auto_advance_last_ms = time.ticks_ms()

        else:
            if reconnecting:
                dd.masterReset()
                led = None
                auto_advance_tab = None
                advance_button = None
                r_7seg_layer = None
                g_7seg_layer = None
                b_7seg_layer = None
                color_layer = None
                r_slider_layer = None
                g_slider_layer = None
                b_slider_layer = None
                auto_advance = None
                auto_advance_last_ms = None

    now_ms = time.ticks_ms()

    if LED is not None:
        led_diff_ms = now_ms - led_last_ms
        if led_diff_ms >= 1000:
            if led is not None:
                led.toggle()
            if LED.value():
                LED.off()
            else:
                LED.on()
            led_last_ms = now_ms


    reset = False
    if led is not None:
        fb: Feedback = led.getFeedback()
        if fb and fb.type == "doubleclick":
            reset = True
            # r_slider_layer.moveToPos(r, 0)
            # g_slider_layer.moveToPos(g, 0)
            # b_slider_layer.moveToPos(b, 0)



    if auto_advance_tab is not None:

        if reset or auto_advance is None or auto_advance_tab.getFeedback():
            if reset:
                auto_advance = False
            else:
                if auto_advance is None:
                    auto_advance = False  # initially, manual advance
                else:
                    auto_advance = not auto_advance
            if auto_advance:
                auto_advance_tab.border(1, "blue", "round")
                auto_advance_tab.pixelColor("red")
                auto_advance_tab.bgPixelColor("green")
                advance_button.disabled(True)
            else:
                auto_advance_tab.border(1, "blue", "hair")
                auto_advance_tab.pixelColor("darkgray")
                auto_advance_tab.bgPixelColor("gray")
                advance_button.disabled(False)

        advance = False
        if auto_advance:
            # check if need to auto advance the colors of the pixels
            diff_ms = now_ms - auto_advance_last_ms
            if diff_ms >= 200:
                # if it has been 200ms, auto advance the colors of the pixels
                advance = True
                auto_advance_last_ms = now_ms
        else:
            if advance_button.getFeedback():
                # if advance button is clicked (has "feedback"), advance the colors of the pixels
                advance = True

        if NP is not None:
            if reset:
                for i in range(NUM_PIXELS):
                    NP[i] = (0, 0, 0)
                NP.write()
            else:
                if advance:
                    # shift pixels colors ... the 1st one will then be set to the color of (r, g, b)
                    for i in range(NUM_PIXELS - 1, 0, -1):
                        NP[i] = NP[i - 1]
                    use_r = int(r * BRIGHTNESS / 255)
                    use_g = int(g * BRIGHTNESS / 255)
                    use_b = int(b * BRIGHTNESS / 255)
                    if r > 0 and use_r == 0:
                        use_r = 1
                    if g > 0 and use_g == 0:
                        use_g = 1
                    if b > 0 and use_b == 0:
                        use_r = 1
                    NP[0] = (use_r, use_g, use_b)
                    NP.write()

        old_r = r
        old_g = g
        old_b = b
        sync_sliders = False

        if reset:
            r = 0
            g = 0
            b = 0
            sync_sliders = True
        else:
            fb: Feedback = r_slider_layer.getFeedback()
            if fb:
                # if there is "feedback" from the R slider, its x position will be the new value for r
                r = fb.x
            fb: Feedback = g_slider_layer.getFeedback()
            if fb:
                # if there is "feedback" from the G slider, its x position will be the new value for g
                g = fb.x
            fb: Feedback = b_slider_layer.getFeedback()
            if fb:
                # if there is "feedback" from the B slider, its x position will be the new value for b
                b = fb.x
            fb: Feedback = color_layer.getFeedback()
            if fb:
                # if there is "feedback" from the color layer, its x position will be the new value for r, and its y position will be the new value for g
                r = fb.x
                g = fb.y
                sync_sliders = True

        if r != old_r or g != old_g or b != old_b:
            # set the background color of the color layer to the new (r, g, b) color
            color_layer.backgroundColor(RGB_COLOR(r, g, b))
            # shows the R/G/B values on the 7-seg layers
            r_7seg_layer.showHexNumber(r)
            g_7seg_layer.showHexNumber(g)
            b_7seg_layer.showHexNumber(b)
            if sync_sliders:
                # check to see if RGB needs to be synced with the sliders
                if r != old_r:
                    r_slider_layer.moveToPos(r, 0)
                if g != old_g:
                    g_slider_layer.moveToPos(g, 0)
                if b != old_b:
                    b_slider_layer.moveToPos(b, 0)
