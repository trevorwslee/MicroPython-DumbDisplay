import time

from ._ddiobase import DDInputOutput
from ._ddlayer import DDLayer

if not 'ticks_ms' in dir(time):
  time.ticks_ms = lambda: int(time.time_ns() / 1000000)
if not 'sleep_ms' in dir(time):
  time.sleep_ms = lambda ms: time.sleep(ms / 1000)


_DD_SID = 'MicroPython-c2'

_DBG_TNL = False

_HS_GAP: int = 1000


class IOProxy:
  def __init__(self, io):
    self._io = io
    self.data: str = ''
  def available(self):
    done = '\n' in self.data
    while (not done) and self._io.available():
      s = self._io.read()
      self.data = self.data + s
      done = '\n' in s
    return done
  def read(self) -> str:
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

_NextLayerNid: int = 0
def _AllocLayerNid():
  global _NextLayerNid
  layerNid = _NextLayerNid
  _NextLayerNid += 1
  return layerNid


class DumbDisplayImpl:
  def __init__(self, io: DDInputOutput):
    self._io: DDInputOutput = io
    self._connected = False
    self._compatibility = 0
    self._connected_iop: IOProxy = None
    self._layers: dict[DDLayer] = {}
    self._tunnels: dict = {}
    
  def timeslice(self):
    self._checkForFeedback()

  def delay(self, seconds: float = 0):
    self.delay_ms(seconds * 1000)

  def delay_ms(self, ms: int = 0):
    self._checkForFeedback()
    until_ms = int(time.ticks_ms() + ms)
    while True:
      remain_ms = until_ms - time.ticks_ms()
      if remain_ms <= 0:
        break
      sleep_ms = 20
      if sleep_ms > remain_ms:
        sleep_ms = remain_ms
      time.sleep_ms(sleep_ms)
      self._checkForFeedback()

  def release(self):
    layers = set(self._layers.values())
    for layer in layers:
      layer.release()
    tunnels = set(self._tunnels)
    for tunnel in tunnels:
      tunnel.release()  
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
  def _allocTunnelNid(self) -> int:
    self._connect()
    tunnel_nid = _AllocLayerNid()
    return tunnel_nid
  def _createLayer(self, layer_type: str, *params) -> str:
    layer_id = str(self._allocLayerNid())
    self._sendCommand(layer_id, "SU", layer_type, *params)
    return layer_id
  def _reorderLayer(self, layer_id: str, how: str): {
    self._sendCommand(layer_id, "REORD", how)
  }   
  def _deleteLayer(self, layer_id: str):
    self._sendCommand(layer_id, "DEL")
  def _onCreatedLayer(self, layer: DDLayer):
    self._layers[layer.layer_id] = layer
  # def _onCreatedLayer(self, layer):
  #   self.layers[layer.layer_id] = layer
  def _onDeletedLayer(self, layer_id: str):
    del self._layers[layer_id]

  # def _ensureConnectionReady(self):
  #   if self._connected:
  #     return
  #   self._io.preconnect()
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
        next_time = now + _HS_GAP
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
          iop.print('>init>:' + _DD_SID + '\n')
          self.toggleDebugLed()
          next_time = now + _HS_GAP
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

  def _sendSpecial(self, special_type: str, special_id: str, special_command: str, special_data: str):
    ##print("lt:" + str(special_command) + ":" + str(special_data))#####
    self.switchDebugLed(True)
    self._io.print('%%>')
    self._io.print(special_type)
    self._io.print('.')
    self._io.print(special_id)
    if special_command != None:
      self._io.print(':')
      self._io.print(special_command)
    self._io.print('>')
    if special_data != None:
      self._io.print(special_data)
    self._io.print('\n')
    self.switchDebugLed(False)
  def _sendCommand(self, layer_id: str, command: str, *params):
    self._checkForFeedback()
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



  def _checkForFeedback(self):
    feedback = self._readFeedback()
    if feedback != None:
      if len(feedback) > 0:
        if feedback[0:1] == '<':
          if len(feedback) == 1:
            self._onFeedbackKeepAlive()
          else:
            #print(feedback)####
            if feedback.startswith('<lt.'):
              try:
                feedback = feedback[4:]
                idx = feedback.find('<')
                if idx != -1:
                  tid = feedback[0:idx]
                  data = feedback[idx + 1:]
                  final = False
                  idx = tid.find(':')
                  if _DBG_TNL:
                    print("** TUNNEL: " + str(idx) + "/" + str(tid) + "/" + str(data))####
                  command = None  
                  if idx != -1:
                    command = tid[idx + 1:]
                    tid = tid[0:idx]
                    if command == "final":
                      final = True
                    elif command == "error":
                      final = True
                      data = ""
                    else:
                      data = "???" + command + "???"
                  #print("##" + str(final) + "/" + str(command) + "/" + str(data))####    
                  tunnel = self._tunnels.get(tid)
                  if tunnel != None:
                    tunnel._handleInput(data, final)
              except:
                pass
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
              layer = self._layers.get(lid)
              if layer != None:
                layer._handleFeedback(type, x, y)
            except:
              pass
  def _readFeedback(self) -> str:
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

  def _createTunnel(self, end_point):
    tunnel_id = str(self._allocTunnelNid())
    self._sendSpecial("lt", tunnel_id, "connect", end_point)
    return tunnel_id
  def _reconnectTunnel(self, tunnel_id, end_point):
    self._sendSpecial("lt", tunnel_id, "reconnect", end_point)
  def _onCreatedTunnel(self, tunnel):
    self._tunnels[tunnel.tunnel_id] = tunnel
  def _onDeletedTunnel(self, tunnel_id):
      del self._tunnels[tunnel_id]

  # def _lt_read(self, tunnel):
  #   self._checkForFeedback()
  #   if len(tunnel._buffer) > 0:
  #     return tunnel._buffer.pop(0)
  #   else:
  #     return None
  # def _lt_send(self, tunnel_id, data):
  #   self._sendSpecial("lt", tunnel_id, None, data)
