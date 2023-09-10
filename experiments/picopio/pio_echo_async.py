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
    mov(x, osr)     # Move the value from the OSR to the X scratch register
    nop() [9]       # Wait for 10 cycles
    mov(isr, x)     # Move the value from the X scratch register to the ISR
    push()          # Push the value from the ISR to the FIFO

# Instantiate a state machine with the wait program, at 2000Hz
sm = rp2.StateMachine(0, wait_prog, freq=2000)

# Activate the state machine
sm.active(1)

# Send a number to the state machine
sm.put(123)
sm.put(578)
sm.put(9999)
sm.put(1111)
sm.put(2222)

# Wait for a moment to let the state machine process the number
#time.sleep(0.01)

if False:
    # Get the result back from the state machine
    print("Result:", sm.get())  # Will print: Result: 123
    # Get the result back from the state machine
    print("Result:", sm.get())  # Will print: Result: 578
    # Get the result back from the state machine
    print("Result:", sm.get())  # Will print: Result: 9999
    # Get the result back from the state machine
    print("Result:", sm.get())  # Will print: Result: 1111
    # Get the result back from the state machine
    print("Result:", sm.get())  # Will print: Result: 2222
else:
    while True:
        # if data is available
        if not sm.empty():  
            data = sm.get()
            print("Data received:", data)
        #await asyncio.sleep(0)  # Yield to other tasks    

# Deactivate the state machine
sm.active(0)







