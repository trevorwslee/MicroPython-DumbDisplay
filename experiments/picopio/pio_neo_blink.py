# https://docs.micropython.org/en/latest/library/rp2.html

import time
import rp2
from machine import Pin

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
    set(pins, 1).delay(15)
    set(pins, 0).delay(8)
    jmp("bit_end")
    label("bit_0")
    set(pins, 1).delay(7)
    set(pins, 0).delay(16)
    label("bit_end")
    jmp(x_dec, "loop_pixel_bit") # x is bit counter
    mov(y, isr)                  # y <= isr (pixel counter)
    jmp(y_dec, "loop_pixel")     # y is pixel counter
    label("debug")
    set(y, 8)
    label("debug_2")
    mov(isr, y)
    push()

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
    res = sm.get()
    print(f"got result {res}")
    
NUM_PIXELS = 4
Pixels = []
for i in range(NUM_PIXELS):
    Pixels.append(None)

Pixels[0] = (128, 0, 0)
Pixels[1] = (0, 128, 0)
Pixels[2] = (0, 0, 128)
Pixels[3] = (32, 32, 32)
ShowNeoPixels(*Pixels)    
    