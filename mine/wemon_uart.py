from machine import Pin,UART
import time


led = Pin(2, Pin.OUT)

try:
    uart = UART(2, 9600)
    uart.init(9600, bits=8, parity=None, stop=1, tx=16, rx=17)
    while True:
        uart.write('hello\n')
        print('hello')
        led.value(not led.value())
        time.sleep(2)
except:    
    while True:
        led.value(not led.value())
        time.sleep(0.5)
    

