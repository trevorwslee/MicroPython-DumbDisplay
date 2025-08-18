from .ddimpl import DumbDisplayImpl
from .ddiobase import DDInputOutput
from .ddlayer import _DD_INT_ARG, _DD_BOOL_ARG, DDLayer

import sys

# try:
#   from machine import Pin
#   _DD_HAS_LED = True
# except:
#   _DD_HAS_LED = False


class DDAutoPin:
  def __init__(self, orientation: str, *layers):
    '''
    :param orientation: H or V or S
    :param layers: layer or "pinner"
    '''
    self.orientation = orientation
    self.layers = layers
  def build(self) -> str:
    return self._build_layout()
  def pin(self, dd):
    layout_spec = self._build_layout()
    dd.configAutoPin(layout_spec)
  def _build_layout(self) -> str:
    layout_spec = None
    for layer in self.layers:
      if layout_spec is None:
        layout_spec = ''
      else:
        layout_spec += '+'
      if type(layer) == DDAutoPin or type(layer) == DDPaddedAutoPin:
        layout_spec += layer._build_layout()
      else:
        layout_spec += layer.layer_id
    if layout_spec is not None:
      layout_spec = str(self.orientation) + '(' + layout_spec + ')'
    else:
      layout_spec = str(self.orientation) + '(*)'
    return layout_spec

class DDPaddedAutoPin(DDAutoPin):
  def __init__(self, orientation: str, left: int, top: int, right: int, bottom: int, *layers):
    self.left = left
    self.top = top
    self.right = right
    self.bottom = bottom
    super().__init__(orientation, *layers)
  def _build_layout(self) -> str:
    layout_spec = super()._build_layout()
    return f"S/{self.left}-{self.top}-{self.right}-{self.bottom}({layout_spec})"


class DumbDisplay(DumbDisplayImpl):
  @staticmethod
  def runningWithMicropython():
    return hasattr(sys, 'implementation') and sys.implementation.name == 'micropython'
  def __init__(self, io: DDInputOutput = None, reset_machine_when_failed_to_send_command: bool = False, reset_machine_if_detected_disconnect_for_s: int = None):
    super().__init__(io)
    #self.debug_led = None
    self.reset_machine_when_failed_to_send_command = reset_machine_when_failed_to_send_command
    self.reset_machine_if_detected_disconnect_for_s = reset_machine_if_detected_disconnect_for_s # _DD_HAS_LED and len(sys.argv) != 0
    self.passive_state = None # None; "cing" (connecting); "c" (connected); "nc" (not connected)

  # def debugSetup(self, debug_led_pin):
  #   '''setup debug use flashing LED pin number'''
  #   if _DD_HAS_LED:
  #     self.debug_led = Pin(debug_led_pin, Pin.OUT)
  def connect(self):
    '''explicit connect'''
    self._connect()
  def connectPassive(self) -> (bool, bool):
    '''
    will use a thread to connect
    :return: (connected, reconnecting) ... reconnecting is True when connected but detected connection loss
    '''
    if self.passive_state is None:
      self.passive_state = "cing"
      try:
        self._connect_threaded_async()
      except Exception as e:
        print(f"xxx Error (connectPassive) -- {e}")
        self.passive_state = None
    if self.passive_state == "c":
      self.timeslice()
      return (True, False)  # connected / not reconnecting
    if self.passive_state == "nc":
        return (True, True)
    if self.passive_state == "cing":
      if self._checked_connect_threaded_async():
        self.passive_state = "c"
        return (True, False)
    return (False, False)
  def masterReset(self):
    self._master_reset()
    self.passive_state = None
  def isReconnecting(self) -> bool:
    iop = self._connected_iop
    return iop is not None and iop.reconnecting
  def autoPin(self, orientation: str = 'V'):
    '''
    auto pin layers
    :param orientation: H or V
    '''
    layout_spec = str(orientation) + '(*)'
    self.configAutoPin(layout_spec)
  def configAutoPin(self, layout_spec: str = "V(*)"):
    '''
    configure "auto pinning of layers" with the layer spec provided
    - horizontal: H(*)
    - vertical: V(*)
    - or nested, like H(0+V(1+2)+3)
    - where 0/1/2/3 are the layer ids
    '''
    self._connect()
    self._sendCommand(None, "CFGAP", layout_spec)
  def addRemainingAutoPinConfig(self, rest_layout_spec: str):
    '''
    add REST "auto pinning" spec for layers not already associated into existing "auto pinning" config
    '''
    self._sendCommand(None, "ADDRESTAP", rest_layout_spec)
  def deleteAllRemainingAutoPinConfigs(self, rest_layout_spec: str):
    '''
    delete all REST "auto pinning" specs
    '''
    self._sendCommand(None, "ADDRESTAP", rest_layout_spec)
  def configPinFrame(self, x_unit_count: int, y_unit_count: int):
    self._connect()
    self._sendCommand(None, "CFGPF", _DD_INT_ARG(x_unit_count), _DD_INT_ARG(y_unit_count))
  # def pinLayer(self, layer_id: str, u_left: int, u_top: int, u_width: int, u_height: int, align: str = ""):
  #   self._sendCommand(layer_id, "PIN", _DD_INT_ARG(u_left), _DD_INT_ARG(u_top), _DD_INT_ARG(u_width), _DD_INT_ARG(u_height), align)
  def pinLayer(self, layer: DDLayer, u_left: int, u_top: int, u_width: int, u_height: int, align: str = ""):
    self._sendCommand(layer.layer_id, "PIN", _DD_INT_ARG(u_left), _DD_INT_ARG(u_top), _DD_INT_ARG(u_width), _DD_INT_ARG(u_height), align)
  def pinAutoPinLayers(self, layout_spec: str, u_left: int, u_top: int, u_width: int, u_height: int, align: str = ""):
    self._sendCommand(None, "PINAP", layout_spec, _DD_INT_ARG(u_left), _DD_INT_ARG(u_top), _DD_INT_ARG(u_width), _DD_INT_ARG(u_height), align)
  def freezeDrawing(self):
    self._connect()
    self._sendCommand(None, "FRZ")
  def unfreezeDrawing(self, refreeze_after_draw: bool = False):
    self._connect()
    self._sendCommand(None, "UNFRZ", _DD_BOOL_ARG(refreeze_after_draw))
  def recordLayerSetupCommands(self):
    self._connect()
    self._sendCommand(None, "RECC")
  def playbackLayerSetupCommands(self, layer_setup_persist_id: str):
    self._sendCommand(None, "SAVEC", layer_setup_persist_id, _DD_BOOL_ARG(True))
    self._sendCommand(None, "PLAYC")
    self._setReconnectRCId(layer_setup_persist_id)
  def recordLayerCommands(self):
    self._connect()
    self._sendCommand(None, "RECC")
  def playbackLayerCommands(self):
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
  def log(self, log_msg: str, is_error: bool = False):
    '''log to DD'''
    if is_error:
      print("X " + log_msg)
    else:
      print("# " + log_msg)
    if self._connected:
      if is_error:
        self._sendCommand(None, '//X ' + log_msg)
      else:
        self._sendCommand(None, '// ' + log_msg)
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

  def tone(self, freq: int, duration: int):
    self._sendCommand(None, "TONE", _DD_INT_ARG(freq), _DD_INT_ARG(duration))
  def notone(self):
    self._sendCommand(None, "NOTONE")

  # def setRootLayer(self, width: int, height: int, contained_alignment: str = "") -> DDLayerGraphical:
  #   /// note that the "root" will always be placed as the container, and hence don't need be pined;
  #   /// @param containedAlignment the alignment of the contained layers; "L" / "T" / "LT"; "" means centered
  #   /// currently, "container" layer does not support "feedback"
  #   /// @since v0.9.9-r50
  #   GraphicalDDLayer* setRootLayer(int width, int height, const String& containedAlignment = "");
  #



  def onDetectedDisconnect(self, for_ms: int):
    if self.passive_state == "c":
      self.passive_state = "nc"
    if self.reset_machine_if_detected_disconnect_for_s and for_ms >= (1000 * self.reset_machine_if_detected_disconnect_for_s):
      print("xxxxxxxxx")
      print("xxx detected disconnection ==>")
      try:
        print("xxx x reset machine")
        import machine
        machine.reset()
      except:
        print("xxx x exit system")
        sys.exit()
  def onSendCommandException(self, error):
    if self.passive_state == "c":
      self.passive_state = "nc"
    print("xxx Error (send command) -- " + str(error))
    if self.reset_machine_when_failed_to_send_command:
      try:
        print("xxx x reset machine")
        import machine
        machine.reset()
      except:
        print("xxx x exit system")
        sys.exit()
    # if self.reset_machine_on_connection_error:
    #   print("xxxxxxxxx")
    #   print("xxx Error (send command) -- {}".format(error))
    #   print("xxxxxxxxx")
    #   try:
    #     print("xxx reset machine")
    #     import machine
    #     machine.reset()
    #   except:
    #     print("xxx exit system")
    #     sys.exit()
    # if _DD_HAS_LED and self.reset_machine_on_connection_error:
    #   import machine
    #   machine.reset()
    # else:
    #   sys.exit()





