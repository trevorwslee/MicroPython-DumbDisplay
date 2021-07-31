
from machine import Pin, PWM

class BlinkTest:
  def __init__(self, pin, pin2, pin_pwm):
    self.led = Pin(pin, Pin.OUT)
    self.led.off()

    self.led2 = Pin(pin2, Pin.OUT)
    self.led2.on()

    self.led_pwm = PWM(Pin(pin_pwm), 1000)
    self.led_pwm.duty(1023)
    
  def once(self):
    self.led.value(not self.led.value())
    self.led2.value(not self.led2.value())
  
    duty = self.led_pwm.duty() - 64
    if duty < 0:
      duty = 1023
    self.led_pwm.duty(duty)
  
from time import sleep

blinkTest = BlinkTest(2, 19, 18)

while True:
  print("*** hello ***")
  blinkTest.once()
  sleep(0.5)  
  