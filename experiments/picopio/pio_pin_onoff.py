
import time
import rp2
from machine import Pin
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def pin_onoff():
    wrap_target()
    set(pins, 1)   # high
    set(pins, 0)   # low
    wrap()
sm = rp2.StateMachine(0, pin_onoff, freq=4000, set_base=Pin(5))
sm.active(1)
time.sleep(1)
sm.active(0)

# import machine
# speaker = machine.Pin(5)
# while True:
#   speaker.on()
#   speaker.off()