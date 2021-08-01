import time
if not 'ticks_ms' in dir(time):
  time.ticks_ms = lambda: int(time.time_ns() / 1000000)


HAND_SHAKE_GAP = 1000


class IOProxy:
  def __init__(self, io):
    self._io = io
    self.data = ''
  def available(self):
    done = False
    while (not done) and self._io.available():
      c = self._io.read()
      if c == '\n':
        done = True
      else:
        self.data = self.data + c
    return done
  def get(self):
    return self.data  
  def clear(self):
    self.data = ''
  def print(self, s):
    self._io.print(s)

_NextLayerNid = 0
def _AllocLayerNid():
  global _NextLayerNid
  layerNid = _NextLayerNid
  _NextLayerNid += 1
  return layerNid


class DumbDisplayImpl:
  def __init__(self, io):
    self._io = io
    self._connected = False
    self._compatibility = 0
    self._connected_iop = None

  def delay(self, seconds = 0):
    self._handleFeedback()
    until_ms = int(time.ticks_ms() + 1000 * seconds)
    while True:
      remain_ms = until_ms - time.ticks_ms()
      if remain_ms <= 0:
        break
      sleep_ms = 20
      if sleep_ms > remain_ms:
        sleep_ms = remain_ms
      time.sleep(sleep_ms / 1000)
      self._handleFeedback()

  def release(self):
    if self._io != None:
      self._io.close()
    self._io = None
    self._connected = False
    self._connected_iop = None

  def toggleDebugLed(self):
    pass
  def switchDebugLed(self, on):
    pass
  def onSendCommandException(self, os_error):
    pass

  def _allocLayerNid(self):
    self._connect()
    layer_nid = _AllocLayerNid()
    return layer_nid

  def _createLayer(self, layer_type, *params):
    layer_id = str(self._allocLayerNid())
    self._sendCommand(layer_id, "SU", layer_type, *params)
    return layer_id

  def _deleteLayer(self, layer_id):
    self._sendCommand(layer_id, "DEL")

  def _connect(self):
    if self._connected:
      return

    self.switchDebugLed(True)
    self._io.preconnect()

    # > ddhello and < ddhello
    iop = IOProxy(self._io)
    next_time = 0
    while True:
      now = time.ticks_ms()
      if now > next_time:
        iop.print('ddhello\n')
        self.toggleDebugLed()
        next_time = now + HAND_SHAKE_GAP
      if iop.available():
        data = iop.get()
        if data == "ddhello":
          self._connected_iop = iop
          break
    iop.clear()

    # > >init> and < <init<  
    compatibility = 0  
    next_time = 0  
    while True:
      now = time.ticks_ms()
      if now > next_time:
          iop.print('>init>:MicroPython-c1\n')
          self.toggleDebugLed()
          next_time = now + HAND_SHAKE_GAP
      if iop.available():
        data = iop.get()
        if data == '<init<':
          break
        if data.startswith('<init<:'):
          compatibility = int(data[data.index(':') + 1:])
          break
    iop.clear()

    self._connected = True  
    self._compatibility = compatibility
    self.switchDebugLed(False)


  def _sendCommand(self, layer_id, command, *params):
    self._handleFeedback()
    self.switchDebugLed(True)
    try:
      if layer_id != None:
        self._io.print(layer_id)
        self._io.print('.')
      self._io.print(command)
      for i in range(0, len(params)):
        if i == 0:
          self._io.print(':')
        else:
          self._io.print(',')
        self._io.print(params[i])
    except OSError as e:
      self.switchDebugLed(False)
      self.onSendCommandException(e)
    self._io.print('\n')
    self.switchDebugLed(False)



  def _handleFeedback(self):
    feedback = self._readFeedback()
    if feedback != None:
      if len(feedback) > 0:
        if feedback[0:1] == '<':
          self._onFeedbackKeepAlive()
        else:
          self._onFeedback(feedback[1:])
  def _readFeedback(self):
    if not self._connected_iop.available():
      return None
    feedback = self._connected_iop.get()
    self._connected_iop.clear()
    return feedback
  def _onFeedbackKeepAlive(self):
    pass
  def _onFeedback(self, feedback):
    print("FB: " + feedback)

