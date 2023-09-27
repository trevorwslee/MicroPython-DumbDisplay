# https://docs.micropython.org/en/latest/library/rp2.html


import time
import rp2
from machine import Pin

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)

def wave_prog():
    pull(block)
    mov(x, osr)  # waves
    pull(block)
    label("loop")
    mov(y, osr)  # wave half len # cycles
    set(pins, 1) # high
    label("high")
    jmp(y_dec, "high")
    mov(y, osr)  # wave half len # cycles
    set(pins, 0) # low
    label("low")
    jmp(y_dec, "low")
    jmp(x_dec, "loop")
    set(x, 1)
    mov(isr, x)
    push()

# Instantiate a state machine with the wait program, at 2000Hz
sm = rp2.StateMachine(0, wave_prog, freq=10000, set_base=Pin(15))


def HWPlayTone(freq: int, duration: int):
    halfWaveNumCycles = int(10000 / freq / 2)    
    waveCount = int(duration / freq / 2)
    print("halfWaveNumCycles", halfWaveNumCycles)
    print("waveCount", waveCount)
    sm.active(1)
    start_ms = time.ticks_ms()
    sm.put(waveCount)
    sm.put(halfWaveNumCycles) # 2 * (x / 10) == blink time
    res = sm.get()
    taken_ms = time.ticks_ms() - start_ms
    print(f"got result {res} in {taken_ms:.2} ms")
    sm.active(0)

if True:

    HWPlayTone(1, 2)

else:    

    # Activate the state machine
    sm.active(1)

    start_ms = time.ticks_ms()
    sm.put(2)
    sm.put(10000) # 2 * (x / 10) == blink time
    res = sm.get()
    taken_ms = time.ticks_ms() - start_ms
    print(f"got result {res} in {taken_ms:.2} ms")
    sm.active(0)




