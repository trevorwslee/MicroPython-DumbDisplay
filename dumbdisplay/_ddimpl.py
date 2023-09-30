import time, _thread

from ._ddiobase import DDInputOutput
from ._ddlayer import DDLayer

if not 'ticks_ms' in dir(time):
  time.ticks_ms = lambda: int(time.time_ns() / 1000000)
if not 'sleep_ms' in dir(time):
  time.sleep_ms = lambda ms: time.sleep(ms / 1000)


_DD_SID = 'MicroPython-c2'

_DBG_TNL = False

_HS_GAP: int = 1000

_RECONNECT_NO_KEEP_ALIVE_MS: int = 5000
_VALIDATE_GAP: int = 1000
_RECONNECTING_VALIDATE_GAP: int = 500


class IOProxy:
  def __init__(self, io):
    self._io = io
    self.data: str = ''
    self.last_keep_alive_ms = 0
    self.reconnect_keep_alive_ms = 0
    self.reconnecting = False
    self.reconnect_enabled = False
    self.reconnect_RC_id = None
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
  def keepAlive(self):
    self.last_keep_alive_ms = time.ticks_ms()
  def setReconnectRCId(self, rc_id: str):
    ### reconnect not working yet
    self.reconnect_RC_id = rc_id
    self.reconnect_enabled = True
    self.reconnect_keep_alive_ms = 0
  def validateConnection(self) -> bool:
    #print("validateConnection")
    keep_alive_diff_ms = None
    need_reconnect = False
    if self.last_keep_alive_ms > 0:
      now = time.ticks_ms()
      keep_alive_diff_ms = now - self.last_keep_alive_ms
      if keep_alive_diff_ms > _RECONNECT_NO_KEEP_ALIVE_MS:
        need_reconnect = True
    if True:
      if need_reconnect:
        if self.reconnect_enabled:
          # reconnecting not working yet
          print(f"detected disconnection ... [{self.reconnect_RC_id}] ... for {keep_alive_diff_ms} ms")
          #print("disconnected ... reconnecting ... ", self.reconnect_RC_id, diff_ms)
        else:
          print(f"detected disconnection ... for {keep_alive_diff_ms} ms")
      elif self.reconnecting:
        print("recovered connection")
    if need_reconnect:
      self.reconnecting = True
    if need_reconnect and self.reconnect_enabled:
      try:
        self._io.print("%%>RECON>")
        self._io.print(_DD_SID)
        self._io.print(":")
        self._io.print(self.reconnect_RC_id)
        self._io.print("\n")
      except:
        pass
      self.reconnect_keep_alive_ms = self.last_keep_alive_ms
    elif self.reconnect_keep_alive_ms > 0:
      self.reconnecting = False
      #_ConnectVersion = _ConnectVersion + 1;
      self.reconnect_keep_alive_ms = 0
      self.last_keep_alive_ms = time.ticks_ms()
    return (need_reconnect, keep_alive_diff_ms)
  def isReconnecting(self) -> bool:
    return self.reconnecting;

_NextLayerNid: int = 0
def _AllocLayerNid():
  global _NextLayerNid
  layerNid = _NextLayerNid
  _NextLayerNid += 1
  return layerNid


def _Connect(io: DDInputOutput):
  io.preconnect()

  # > ddhello and < ddhello
  iop = IOProxy(io)
  next_time = 0
  while True:
    now = time.ticks_ms()
    if now > next_time:
      iop.print('ddhello\n')
      next_time = now + _HS_GAP
    if iop.available():
      data = iop.read()
      if data == "ddhello":
        #self._connected_iop = iop
        break

  compatibility = 0
  next_time = 0
  while True:
    now = time.ticks_ms()
    if now > next_time:
      iop.print('>init>:' + _DD_SID + '\n')
      next_time = now + _HS_GAP
    if iop.available():
      data = iop.read()
      if data == '<init<':
        break
      if data.startswith('<init<:'):
        compatibility = int(data[data.index(':') + 1:])
        break

  return (iop, compatibility)

_ConnectThreadedResult = None
_ConnectThreadedLock = _thread.allocate_lock()
def _Connect_Threaded(io: DDInputOutput):
  global _ConnectThreadedResult
  connect_res = _Connect(io)
  try:
    _ConnectThreadedLock.acquire()
    _ConnectThreadedResult = connect_res
  finally:
    _ConnectThreadedLock.release()


class DumbDisplayImpl:
  def __init__(self, io: DDInputOutput):
    self._io: DDInputOutput = io
    self._connected = False
    self._compatibility = 0
    self._connected_iop: IOProxy = None
    self._layers: dict[DDLayer] = {}
    self._tunnels: dict = {}
    self.last_validate_ms = 0

  def timeslice(self):
    self._checkForFeedback()

  def delay(self, seconds: float = 0):
    '''
    use sleep() instead
    '''
    self.sleep_ms(seconds * 1000)

  def sleep(self, seconds: float = 0):
    self.sleep_ms(seconds * 1000)

  def sleep_ms(self, ms: int = 0):
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


  def _master_reset(self):
    layers = set(self._layers.values())
    for layer in layers:
      layer.release()
    tunnels = set(self._tunnels)
    for tunnel in tunnels:
      tunnel.release()
    if self._io is not None:
      self._io.close()
    # self._io = None
    self._connected = False
    self._connected_iop = None

  def release(self):
    if True:
      self._master_reset()
      if self._io is not None:
        self._io.close()
      self._io = None
    else:
      layers = set(self._layers.values())
      for layer in layers:
        layer.release()
      tunnels = set(self._tunnels)
      for tunnel in tunnels:
        tunnel.release()
      if self._io is not None:
        self._io.close()
      self._io = None
      self._connected = False
      self._connected_iop = None

  # def toggleDebugLed(self):
  #   pass
  # def switchDebugLed(self, on):
  #   pass
  def onDetectedDisconnect(self, for_ms: int):
    pass
  def onSendCommandException(self, error):
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
  def _reorderLayer(self, layer_id: str, how: str):
    self._sendCommand(layer_id, "REORD", how)
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

    if True:
      (iop, compatibility) = _Connect(self._io)
      self._connected_iop = iop
      self._connected = True
      self._compatibility = compatibility
    else:
      #self.switchDebugLed(True)
      self._io.preconnect()

      # > ddhello and < ddhello
      iop = IOProxy(self._io)
      next_time = 0
      while True:
        now = time.ticks_ms()
        if now > next_time:
          iop.print('ddhello\n')
          #self.toggleDebugLed()
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
            #self.toggleDebugLed()
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
      #self.switchDebugLed(False)
      #print('connected:' + str(compatibility))

  def _connect_threaded_async(self):
    if not self._connected:
      _thread.start_new_thread(_Connect_Threaded, (self._io,))

  def _checked_connect_threaded_async(self):
    global _ConnectThreadedResult
    if self._connected:
      return True
    try:
      _ConnectThreadedLock.acquire()
      if _ConnectThreadedResult is not None:
        (iop, compatibility) = _ConnectThreadedResult
        _ConnectThreadedResult = None
        self._connected_iop = iop
        self._connected = True
        self._compatibility = compatibility
        return True
      else:
        return False
    finally:
      _ConnectThreadedLock.release()

  def _sendSpecial(self, special_type: str, special_id: str, special_command: str, special_data: str):
    ##print("lt:" + str(special_command) + ":" + str(special_data))#####
    #self.switchDebugLed(True)
    self._io.print('%%>')
    self._io.print(special_type)
    self._io.print('.')
    self._io.print(special_id)
    if special_command is not None:
      self._io.print(':')
      self._io.print(special_command)
    self._io.print('>')
    if special_data is not None:
      self._io.print(special_data)
    self._io.print('\n')
    #self.switchDebugLed(False)
  def _sendCommand(self, layer_id: str, command: str, *params):
    self._checkForFeedback()
    #self.switchDebugLed(True)
    try:
      if layer_id is not None:
        self._io.print(layer_id)
        self._io.print('.')
      self._io.print(command)
      for i in range(0, len(params)):
        if i == 0:
          self._io.print(':')
        else:
          self._io.print(',')
        self._io.print(params[i])
      self._io.print('\n')
    except Exception as e:
      #self.switchDebugLed(False)
      self.onSendCommandException(e)
    #self._io.print('\n')
    #self.switchDebugLed(False)



  def _checkForFeedback(self):
    feedback = self._readFeedback()
    if feedback is not None:
      if len(feedback) > 0:
        self._onFeedbackSignal()
        if feedback[0:1] == '<':
          #self._onFeedbackKeepAlive()
          if len(feedback) == 1:
            pass
            #self._onFeedbackKeepAlive()
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
                  if tunnel is not None:
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
              if layer is not None:
                layer._handleFeedback(type, x, y)
            except:
              pass
  def _readFeedback(self) -> str:
    (need_reconnect, keep_alive_diff_ms) = self._validateConnection()
    if need_reconnect:
      self.onDetectedDisconnect(keep_alive_diff_ms)
    if not self._connected_iop.available():
      return None
    feedback = self._connected_iop.read()
    #self._connected_iop.clear()
    return feedback
  def _onFeedbackSignal(self):
    if self._connected_iop:
      self._connected_iop.keepAlive()
  def _validateConnection(self):
    if self._connected_iop:
      validate_gap = _RECONNECTING_VALIDATE_GAP if self._connected_iop.isReconnecting() else _VALIDATE_GAP
      now = time.ticks_ms()
      diff_ms = now - self.last_validate_ms
      if diff_ms >= validate_gap:
        (need_reconnect, keep_alive_diff_ms) = self._connected_iop.validateConnection()
        self.last_validate_ms = now
      else:
        (need_reconnect, keep_alive_diff_ms) = (None, None)
      return (need_reconnect, keep_alive_diff_ms)
  def _setReconnectRCId(self, rc_id: str):
    if self._connected_iop:
        self._connected_iop.setReconnectRCId(rc_id)
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
