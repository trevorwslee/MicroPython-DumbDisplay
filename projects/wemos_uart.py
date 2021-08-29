from machine import Pin,UART
import time


led = Pin(2, Pin.OUT)

try:
    uart = UART(2, 115200)
    #uart.init(115200, bits=8, parity=None, stop=1, tx=16, rx=17)
    uart.init(115200, tx=16, rx=17)
    while True:
        uart.write('hello\n')
        if uart.any():
            val = uart.readline().decode('UTF8')
            print(val)
        print('hello')
        led.value(not led.value())
        time.sleep(2)
except:    
    while True:
        led.value(not led.value())
        time.sleep(0.5)
