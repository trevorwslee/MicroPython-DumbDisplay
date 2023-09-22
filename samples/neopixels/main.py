import time


NUM_PIXELS = 4
NEO_PIXELS_IN_PIN = 22

try:

    import rp2
    from machine import Pin

    # bits shifting
    # =============
    # - for the pixels: 1st pixel then 2nd pixel ...
    # - for a pixel (24 bits): G then R then B
    # - for R/G/B (8 bits): most significant bit first
    # timing for a bit:
    # - 0: .4us high + .85us low
    # - 1: .8us high + .45us low
    # if frequency is 20MHz ... i.e. each cycle takes 0.05us
    # - 0: 8 cycles high + 17 cycles low
    # - 1: 16 cycles high + 9 cycles low
    # afterward, delay for 300us

    @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT)  # SHIFT_LEFT: i.e. most significant bit first
    def neo_prog():
        pull()                       # osr <= number of pixels - 1
        mov(y, osr)                  # y <= number of pixels - 1
        label("loop_pixel")
        mov(isr, y)                  # isr (pixel counter) <= y
        pull()                       # sor <= 24 bits GRB
        set(x, 23)                   # x (bit counter) <= 23
        label("loop_pixel_bit")
        out(y, 1)                    # y <= left-most 1 bit of sor
        jmp(not_y, "bit_0")
        set(pins, 1).delay(15)       # 1: high (16 cycles)
        set(pins, 0).delay(8)        # 1: low (9 cycles)
        jmp("bit_end")
        label("bit_0")
        set(pins, 1).delay(7)        # 0: high (8 cycles)
        set(pins, 0).delay(16)       # 0: low (17 cycles)
        label("bit_end")
        jmp(x_dec, "loop_pixel_bit") # x is bit counter
        mov(y, isr)                  # y <= isr (pixel counter)
        jmp(y_dec, "loop_pixel")     # y is pixel counter

    sm = rp2.StateMachine(0, neo_prog, freq=20_000_000, set_base=Pin(NEO_PIXELS_IN_PIN))
    sm.active(1)

    def ShowNeoPixels(*pixels):
        '''
        each pixel is the tuple (r, g, b)
        '''
        pixel_count = len(pixels)
        sm.put(pixel_count - 1)
        for i in range(pixel_count):
            pixel = pixels[i]
            if pixel:
                (r, g, b) = pixel
            else:
                (r, g, b) = (0, 0, 0)
            grb = (g << 16) + (r << 8) + b    # the order is G R B
            sm.put(grb, 8)                    # a word is 32 bits, so, pre-shift out (discard) 8 bits, leaving 24 bits of the GRB
        time.sleep_us(300)                    # make sure the NeoPixels is reset for the next round

    Pixels = []
    for i in range(NUM_PIXELS):
        Pixels.append(None)

except:
    print("Cannot initialize NeoPixels!")
    Pixels = None


from dumbdisplay.core import *
from dumbdisplay.layer_lcd import *
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

# crate a tab (LayerLcd) to control whether auto advance the pixel's color from the previous pixel to the next pixel
auto_advance_tab = LayerLcd(dd, 12, 1)
auto_advance_tab.writeCenteredLine("Auto Advance")
auto_advance_tab.enableFeedback("fl")

# crate a button (LayerLcd) to manually advance the pixel's color from the previous pixel to the next pixel
advance_button = LayerLcd(dd, 3, 1)
advance_button.border(1, "blue", "round")
advance_button.writeCenteredLine(">>>")
advance_button.enableFeedback("fl")

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
        AutoPin('H', auto_advance_tab, advance_button),
        color_layer,
        r_slider_layer,
        g_slider_layer,
        b_slider_layer).pin(dd)

auto_advance = None
r = 0
g = 0
b = 0
color_layer.backgroundColor(RGB_COLOR(r, g, b))
last_ms = time.ticks_ms()

while True:

    if auto_advance is None or auto_advance_tab.getFeedback():
        # if it is not initialized, or if auto advance tab is clicked (has "feedback"), set auto advance accordingly
        if auto_advance is None:
            auto_advance = False  # initially, manual advance
        else:
            auto_advance = not auto_advance
        # set auto advance tab's border, pixel color and background pixel color according to whether auto advance is on or off
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
        diff_ms = time.ticks_ms() - last_ms
        if diff_ms >= 200:
            # if it has been 200ms, auto advance the colors of the pixels
            advance = True
            last_ms = time.ticks_ms()
    else:
        if advance_button.getFeedback():
            # if advance button is clicked (has "feedback"), advance the colors of the pixels
            advance = True

    if Pixels:
        if advance:
            # shift pixels colors ... the 1st one will then be set to the color of (r, g, b)
            for i in range(NUM_PIXELS - 1, 0, -1):
                Pixels[i] = Pixels[i - 1]
            Pixels[0] = (r, g, b)
            ShowNeoPixels(*Pixels)

    old_r = r
    old_g = g
    old_b = b
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

    sync_sliders = False    
    fb: Feedback = color_layer.getFeedback()
    if fb:
        # if there is "feedback" from the color layer, its x position will be the new value for r, and its y position will be the new value for g
        r = fb.x
        g = fb.y
        sync_sliders = True

    if r != old_r or g != old_g or b != old_b:
        # set the background color of the color layer to the new (r, g, b) color
        color_layer.backgroundColor(RGB_COLOR(r, g, b))
        if sync_sliders:
            # check to see if RGB needs to be synced with the sliders
            if r != old_r:
                r_slider_layer.moveToPos(r, 0)
            if g != old_g:
                g_slider_layer.moveToPos(g, 0)
            if b != old_b:
                b_slider_layer.moveToPos(b, 0)
