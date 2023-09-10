import time
import rp2
from machine import Pin


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    set(pins, 1)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    set(pins, 0)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    wrap()

@rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,)*4,
             out_shiftdir=rp2.PIO.SHIFT_RIGHT,
             autopull=True, pull_thresh=4)
def prog():
    pull()
    out(pins, 4)


sm_1 = rp2.StateMachine(0, prog, freq=2000, out_base=Pin(10))
sm_2 = rp2.StateMachine(1, prog, freq=2000, out_base=Pin(18))
blink_sm = rp2.StateMachine(7, blink, freq=2000, set_base=Pin(2))

blink_sm.active(1)
sm_1.active(1)
sm_2.active(1)

val = 0b1111
sm_1.put(val)
sm_2.put(val)
time.sleep(5)

blink_sm.active(0)
sm_1.active(0)
sm_2.active(0)