import time
import rp2
from machine import Pin

@rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,) * 4,
             out_shiftdir=rp2.PIO.SHIFT_RIGHT,
             autopull=True, pull_thresh=4)
def prog():
    pull()
    out(pins, 4)


sm_1 = rp2.StateMachine(0, prog, freq=2000, out_base=Pin(10))
sm_2 = rp2.StateMachine(1, prog, freq=2000, out_base=Pin(18))

sm_1.active(1)
sm_2.active(1)

sm_1.put(0b1111)
sm_2.put(0b0000)
time.sleep(1000)



oo_1 = [ 0b0111, 0b0100, 0b0011, 0b0110, 0b0100, 0b0110, 0b0111, 0b0100, 0b0111, 0b0110, 0b1000, 0b0011 ]
oo_2 = [ 0b0111, 0b0001, 0b1011, 0b1011, 0b1101, 0b1110, 0b1100, 0b0011, 0b1111, 0b1111, 0b0000, 0b1110 ]

for d in range(0, 12):
    sm_1.put(oo_1[d])
    sm_2.put(oo_2[d])
    time.sleep(1)

blink_sm.active(0)
sm_1.active(0)
sm_2.active(0)