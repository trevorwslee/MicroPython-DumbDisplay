from dumbdisplay._ddimpl import DumbDisplayImpl
from dumbdisplay._ddiobase import DDInputOutput
from ._ddlayer import _DD_INT_ARG, _DD_BOOL_ARG


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
  def build(self):
    return self._build_layout()
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
  @staticmethod
  def runningWithMicropython():
    return hasattr(sys, 'implementation') and sys.implementation.name == 'micropython'
  def __init__(self, io: DDInputOutput):
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
  def configPinFrame(self, xUnitCount: int, yUnitCount: int):
    self._connect()
    self._sendCommand(None, "CFGPF", _DD_INT_ARG(xUnitCount), _DD_INT_ARG(yUnitCount))
  def _pinLayer(self, layer_id: str, uLeft: int, uTop: int, uWidth: int, uHeight: int, align: str = ""):
    self._sendCommand(layer_id, "PIN", _DD_INT_ARG(uLeft), _DD_INT_ARG(uTop), _DD_INT_ARG(uWidth), _DD_INT_ARG(uHeight), align)
  def pinAutoPinLayers(self, layout_spec: str, uLeft: int, uTop: int, uWidth: int, uHeight: int, align: str = ""):
    self._sendCommand(None, "PINAP", layout_spec, _DD_INT_ARG(uLeft), _DD_INT_ARG(uTop), _DD_INT_ARG(uWidth), _DD_INT_ARG(uHeight), align)
  def recordLayerSetupCommands(self):
    self._connect()
    self._sendCommand(None, "RECC")
  def playbackLayerSetupCommands(self, layerSetupPersistId: str):
    self._sendCommand(None, "SAVEC", layerSetupPersistId, _DD_BOOL_ARG(True))
    self._sendCommand(None, "PLAYC")
  def backgroundColor(self, color: str):
    '''set DD background color with common "color name"'''
    self._connect()
    self._sendCommand(None, "BGC", color)
  def writeComment(self, comment: str):
    '''write out a comment to DD'''
    self._connect()
    self._sendCommand(None, '// ' + comment)
    print("# " + comment)
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




