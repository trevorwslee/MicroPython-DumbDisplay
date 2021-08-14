from ._ddimpl import DumbDisplayImpl

import sys

try:
  from machine import Pin
  _DD_HAS_LED = True
except:
  _DD_HAS_LED = False


class DDAutoPin:
  def __init__(self, orientation, *layers):
    '''
    :param orientation: H or V
    :param layers: layer or "pinner"
    '''
    self.orientation = orientation
    self.layers = layers
  def pin(self, dd):
    layout_spec = self._build_layout()
    if layout_spec != None:
      dd.configAutoPin(layout_spec)
  def _build_layout(self):
    layout_spec = None
    for layer in self.layers:
      if layout_spec == None:
        layout_spec = ''
      else:
        layout_spec += '+'
      if type(layer) == DDAutoPin:
        layout_spec += layer._build_layout()
      else:
        layout_spec += layer.layer_id
    if layout_spec != None:
      layout_spec = str(self.orientation) + '(' + layout_spec + ")"
    return layout_spec


class DumbDisplay(DumbDisplayImpl):
  def __init__(self, io):
    super().__init__(io)
    self.debug_led = None
    self.reset_machine_on_connection_error = False # _DD_HAS_LED and len(sys.argv) != 0

  def debugSetup(self, debug_led_pin):
    '''setup debug use flashing LED pin number'''
    if _DD_HAS_LED:
      self.debug_led = Pin(debug_led_pin, Pin.OUT)
  def connect(self):
    '''explicit connect'''
    self._connect()
  def autoPin(self, orientation = 'V'):
    '''
    auto pin layers
    :param orientation: H or V
    '''
    layout_spec = str(orientation) + '(*)'
    self.configAutoPin(layout_spec)
  def configAutoPin(self, layout_spec):
    '''
    configure "auto pinning of layers" with the layer spec provided
    - horizontal: H(*)
    - vertical: V(*)
    - or nested, like H(0+V(1+2)+3)
    - where 0/1/2/3 are the layer ids
    '''
    self._connect()
    self._sendCommand(None, "CFGAP", layout_spec)
  def backgroundColor(self, color):
    '''set DD background color with common "color name"'''
    self._connect()
    self._sendCommand(None, "BGC", color)
  def writeComment(self, comment):
    '''write out a comment to DD'''
    self._connect()
    self._sendCommand(None, '// ' + comment)
  def recordLayerCommands(self):
    '''
    start recording layer commands (of any layers)
    and sort of freeze the display, until playback
    '''
    self._sendCommand(None, "RECC")
  def playbackLayerCommands(self):
    '''playback recorded commands (unfreeze the display)'''
    self._sendCommand(None, "PLAYC")
  def release(self):
    '''release it'''
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
  def onSendCommandException(self, os_error):
    print("xxxxxxxxx")
    print("xxx OsError -- " + str(os_error) )
    print("xxxxxxxxx")
    if _DD_HAS_LED and self.reset_machine_on_connection_error:
      import machine
      machine.reset()
    else:
      sys.exit()




