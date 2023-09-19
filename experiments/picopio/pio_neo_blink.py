# https://docs.micropython.org/en/latest/library/rp2.html

import time
import rp2
from machine import Pin


# bits shifting
# . 1st pixel then 2nd pixel ...
# . G then R then B
# . most significant first
# timing for bit:
# . 0: .4us high + .85us low
# . 1: .8us high + .45us low
# if frequency is 20MHz ... i.e. each cycle 0.05us
# . 0: 8 cycles high + 17 cycles low
# . 1: 16 cycles high + 9 cycles low
# afterward, delay for 300us


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT)
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
    # label("debug")
    # set(y, 8)
    # label("debug_2")
    # mov(isr, y)
    # push()

sm = rp2.StateMachine(0, neo_prog, freq=20_000_000, set_base=Pin(22))
sm.active(1)

def ShowNeoPixels(*pixels):
    '''
    each pixel RGB is the tuple (r, g, b)
    '''
    pixel_count = len(pixels)
    sm.put(pixel_count - 1)
    for i in range(pixel_count):
        pixel = pixels[i]
        if pixel:
            (r, g, b) = pixel
        else:
            (r, g, b) = (0, 0, 0)
        grb = (g << 16) + (r << 8) + b  # the order is G R B
        #print(f". [{i}] = {pixel} ({grb})")
        sm.put(grb, 8)
    time.sleep_us(300)
    # res = sm.get()
    # print(f"got result {res}")


NUM_PIXELS = 4
Pixels = []
for i in range(NUM_PIXELS):
    Pixels.append(None)

# Pixels[0] = (128, 0, 0)
# Pixels[1] = (0, 128, 0)
# Pixels[2] = (0, 0, 128)
# Pixels[3] = (32, 32, 32)
# ShowNeoPixels(*Pixels)    
    

rgb = 0
i = 0
while True:
    if rgb == 0:
        c = (255, 0, 0)
    elif rgb == 1:
        c = (0, 255, 0)
    else:
        c = (0, 0, 255)
    Pixels[i] = c
    ShowNeoPixels(*Pixels)
    time.sleep(0.1)
    Pixels[i] = (0, 0, 0)
    ShowNeoPixels(*Pixels)
    rgb = (rgb + 1) % 3
    i = (i + 1) % NUM_PIXELS    