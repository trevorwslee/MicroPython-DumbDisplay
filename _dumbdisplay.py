from _ddimpl import DumbDisplayImpl

try:
  from machine import Pin
  _DD_HAS_LED = True
except:
  _DD_HAS_LED = False

class DumbDisplay(DumbDisplayImpl):
  def __init__(self, io):
    super().__init__(io)
    self.debug_led = None

  def debugSetup(self, debug_led_pin):
    '''setup debug use flashing LED pin number'''
    if _DD_HAS_LED:
      self.debug_led = Pin(debug_led_pin, Pin.OUT)
  def connect(self):
    '''explicit connect'''
    self._connect()
  def backgroundColor(self, color):
    '''set DD background color with common "color name"'''
    self._connect()
    self._sendCommand1(None, "BGC", color)
  def writeComment(self, comment):
    '''write out a comment to DD'''
    self._connect()
    self._sendCommand(None, '// ' + comment)
  def release(self):
    super().release()

  def toggleDebugLed(self):
      if self.debug_led != None:
        self.debug_led.value(not self.debug_led.value())
  def switchDebugLed(self, on):
    if self.debug_led != None:
      if on:
        self.debug_led.on()
      else:
        self.debug_led.off()






