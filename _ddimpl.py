import time
if not 'ticks_ms' in dir(time):
  time.ticks_ms = lambda: int(time.time_ns() / 1000000)
if not 'sleep_ms' in dir(time):
  time.sleep_ms = lambda ms: time.sleep(ms / 1000)


HAND_SHAKE_GAP = 1000


class IOProxy:
  def __init__(self, io):
    self._io = io
    self.data = ''
  def available(self):
    done = '\n' in self.data
    while (not done) and self._io.available():
      s = self._io.read()
      self.data = self.data + s
      done = '\n' in s
    return done
  def read(self):
    #print(self.data)
    idx = self.data.index('\n')
    s = self.data[0:idx]
    self.data = self.data[idx + 1:]  
    #print("*" + self.data + "*")
    return s
  #def get(self):
  #  return self.data  
  #def clear(self):
  #  self.data = ''
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
    self.layers = {}

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
      time.sleep_ms(sleep_ms)
      self._handleFeedback()

  def release(self):
    layers = set(self.layers.values())
    for layer in layers:
      layer.release()
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
  def _onCreatedLayer(self, layer):
    self.layers[layer.layer_id] = layer
  def _onCreatedLayer(self, layer):
    self.layers[layer.layer_id] = layer
  def _onDeletedLayer(self, layer):
    del self.layers[layer.layer_id]

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
        data = iop.read()
        #print(">[" + data + "]")
        if data == "ddhello":
          self._connected_iop = iop
          break
    #iop.clear()

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
        data = iop.read()
        #print('#' + data)
        if data == '<init<':
          break
        if data.startswith('<init<:'):
          compatibility = int(data[data.index(':') + 1:])
          break
    #iop.clear()

    self._connected = True  
    self._compatibility = compatibility
    self.switchDebugLed(False)
    #print('connected:' + str(compatibility))


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
          idx = feedback.find('.')
          if idx != -1:
            try:
              lid = feedback[0:idx]
              feedback = feedback[idx + 1:]
              idx = feedback.index(':')
              type = feedback[0:idx]
              feedback = feedback[idx + 1:]
              idx = feedback.index(',')
              x = int(feedback[0:idx])
              y = int(feedback[idx + 1:])
              layer = self.layers.get(lid)
              if layer != None:
                layer._handleFeedback(type, x, y)
            except:
              pass
  def _readFeedback(self):
    if not self._connected_iop.available():
      return None
    feedback = self._connected_iop.read()
    #self._connected_iop.clear()
    return feedback
  def _onFeedbackKeepAlive(self):
    pass
  # def _onFeedback(self, lid, type, x, y):
  #   layer = self.layers.get(lid)
  #   if layer != None:
  #     layer._handleFeedback(type, x, y)
  #     #print("FB: " + layer.layer_id + '.' + type + ':' + str(x) + ',' + str(y))

