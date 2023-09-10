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

#sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin("LED"))
#sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(25))
sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(15))

sm.active(1)
time.sleep(3)
sm.active(0)