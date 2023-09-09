import time
import rp2
from machine import Pin

# Create a PIO program to read a number, wait for 10 cycles, and then return it
@rp2.asm_pio(
    in_shiftdir=rp2.PIO.SHIFT_LEFT,
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
)

def wait_prog():
    pull(block)     # Pull a number from the FIFO into the OSR
    mov(x, osr)
    mov(y, osr)
    label("delay")   # Label for the delay loop
    jmp(x_dec, "delay") # Jump to the "delay" label if X is not zero, decrementing X each time    mov(isr, x)     # Move the value from the X scratch register to the ISR
    mov(isr, y)      # Move the value from the Y scratch register to the ISR
    push()          # Push the value from the ISR to the FIFO

# Instantiate a state machine with the wait program, at 2000Hz
sm = rp2.StateMachine(0, wait_prog, freq=10000)

# Activate the state machine
sm.active(1)

start_ms = time.ticks_ms()
sm.put(100)
res = sm.get()
taken_ms = time.ticks_ms() - start_ms
print(f"got result {res} in {taken_ms:.2} ms")
sm.active(0)



