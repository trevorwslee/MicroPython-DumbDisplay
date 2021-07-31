from dumbdisplay_impl import DumbDisplayImpl

try:
  from machine import Pin
  HAS_LED = True
except:
  HAS_LED = False

class DumbDisplay(DumbDisplayImpl):
  def __init__(self, io):
    super().__init__(io)
    self.debug_led = None
  def debugSetup(self, debug_led_pin):
    if HAS_LED:
      self.debug_led = Pin(debug_led_pin, Pin.OUT)
  def connect(self):
    self._connect()
  def writeComment(self, comment):
    self._connect()
    self._sendCommand(None, '// ' + comment)

  def toggleDebugLed(self):
    if self.debug_led != None:
        self.debug_led.value(not self.debug_led.value())
  def switchDebugLed(self, on):
    if self.debug_led != None:
      if on:
        self.debug_led.on()
      else:
        self.debug_led.off()






