import time, _thread

from .ddiobase import DDInputOutput
from .ddlayer import DDLayer, _DD_INT_ARG
from .ddcmds import DDC_KAL

# the followings will add time_ms and sleep_ms to the time module ... globally
if not 'ticks_ms' in dir(time):
  time.ticks_ms = lambda: int(time.time_ns() / 1000000)
if not 'sleep_ms' in dir(time):
  time.sleep_ms = lambda ms: time.sleep(ms / 1000)

#_DD_LIB_COMPATIBILITY = 2
#_DD_LIB_COMPATIBILITY = 7   # for :drag
#_DD_LIB_COMPATIBILITY = 8   # for feedback type
#_DD_LIB_COMPATIBILITY = 9   # joy stick valuerange (not used)

#_DD_SID = 'MicroPython-c2'
#_DD_SID = "MicroPython-c9"  # joy stick valuerange (not used)
#_DD_SID = "MicroPython-c14"  # bring forward since v0.5.1
#_DD_SID = "MicroPython-c15"
_DD_SID = "MicroPython-c16"

_ROOT_LAYER_ID = "00"  # hardcoded

_DBG_TNL = False

_HS_GAP: int = 1000

_PASSIVE_CHECK_GAP_MS = 500
_RECONNECT_NO_KEEP_ALIVE_MS: int = 5000
_VALIDATE_GAP: int = 1000
_RECONNECTING_VALIDATE_GAP: int = 500

_INIT_ACK_SEQ = 0

def _NEXT_ACK_SEQ(ack_seq: int) -> int:
  if True:
    ack_seq = (ack_seq + 1) % 62
  else:
    ack_seq = (ack_seq + 1) % 10
  return ack_seq

def _ACK_SEQ_TO_ACK_STR(ack_seq: int) -> str:
  if True:
    if ack_seq < 10:
      return str(ack_seq)
    elif ack_seq < 36:
      return chr(ord('A') + ack_seq - 10)
    else:
      return chr(ord('a') + ack_seq - 36)
  else:
    return str(ack_seq)

def _ACK_STR_TO_ACK_SEQ(ack_str: str) -> int:
    if True:
        if ack_str >= '0' and ack_str <= '9':
          return int(ack_str)
        elif ack_str >= 'A' and ack_str <= 'Z':
          return ord(ack_str) - ord('A') + 10
        elif ack_str >= 'a' and ack_str <= 'z':
          return ord(ack_str) - ord('a') + 36
        else:
          raise ValueError("Invalid ACK string: " + ack_str)
    else:
        return int(ack_str)


def ReadLocalFileBytes(local_file_name: str, parent_path: str = None, resources_id: str = None) -> bytes:
  local_file_bytes = None
  if resources_id is not None:
    try:
      import importlib.resources
      if True:
        with importlib.resources.path(resources_id, local_file_name) as local_file_path:
          with open(local_file_path, "rb") as f:
            local_file_bytes = f.read()
      else:
        resource = importlib.resources.files(resources_id).joinpath(local_file_name)
        if resource.is_file():
          with importlib.resources.path(resources_id, local_file_name) as local_file_path:
            with open(local_file_path, "rb") as f:
              local_file_bytes = f.read()
    except:
      pass
  if local_file_bytes is None and parent_path is not None:
    if parent_path.lower().endswith(".py"):
      parent_path = parent_path.replace("\\", "/")
      parent_path = parent_path[0:parent_path.rfind("/")]
    local_file_path = parent_path + "/" + local_file_name
    with open(local_file_path, "rb") as f:
      local_file_bytes = f.read()
  return local_file_bytes



class IOProxy:
  def __init__(self, io: DDInputOutput):
    self._io = io
    self.data: str = ''
    self.last_keep_alive_ms: int = 0
    self.reconnect_keep_alive_ms: int = 0
    self.reconnecting: bool = False
    self.reconnect_enabled: bool = False
    self.reconnect_RC_id: str = None
  def available(self):
    done = '\n' in self.data
    while (not done) and self._io.available():
      s = self._io.read()
      self.data = self.data + s
      done = '\n' in s
    return done
  def read(self) -> str:
    # if True:  # TODO: disable printing of received data
    #   data = self.data[:-1]
    #   print(data)
    idx = self.data.index('\n')
    s = self.data[0:idx]
    self.data = self.data[idx + 1:]  
    #print("*" + self.data + "*")
    return s
  #def get(self):
  #  return self.data  
  #def clear(self):
  #  self.data = ''
  def print(self, s: str):
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
  try:
      connect_res = _Connect(io)
      try:
        _ConnectThreadedLock.acquire()
        _ConnectThreadedResult = connect_res
      finally:
        _ConnectThreadedLock.release()
  except Exception as e:
      print("xxx Error (send command) -- " + str(e))


class DumbDisplayImpl:
  def __init__(self, io: DDInputOutput):
    if io is None:
      # if not specific, default to DDIOInet
      from .ddio_inet import DDIOInet
      io = DDIOInet()
    self._io: DDInputOutput = io
    self._connected = False
    self._compatibility = 0
    self._connected_iop: IOProxy = None
    self._root_layer = None
    self._layers: dict[str, DDLayer] = {}
    self._tunnels: dict = {}
    self.last_validate_ms = 0

  def getCompatibility(self) -> int:
    return self._compatibility


  def timeslice(self):
    self._checkForFeedback()

  def delay(self, seconds: float = 0):
    """
    deprecated; use sleep() instead
    """
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


  def _master_reset(self, keep_connected: bool = False):
    if self._root_layer is not None:
      self._root_layer.release()
    layers = set(self._layers.values())
    for layer in layers:
      layer.release()
    tunnels = set(self._tunnels)
    for tunnel in tunnels:
      tunnel.release()
    if not keep_connected:
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
  def _setRootLayer(self, width: int, height: int, contained_alignment: str) -> str:
    if self._root_layer is not None:
      self._root_layer.release()
    self._connect()
    self._sendCommand(None, "ROOT", _DD_INT_ARG(width), _DD_INT_ARG(height), contained_alignment);
    layer_id = _ROOT_LAYER_ID
    return layer_id
  def _reorderLayer(self, layer_id: str, how: str):
    self._sendCommand(layer_id, "REORD", how)
  def _deleteLayer(self, layer_id: str):
    self._sendCommand(layer_id, "DEL")
  def _onCreatedLayer(self, layer: DDLayer):
    if layer.layer_id == _ROOT_LAYER_ID:
      _root_layer = layer
    else:
      self._layers[layer.layer_id] = layer
  # def _onCreatedLayer(self, layer):
  #   self.layers[layer.layer_id] = layer
  def _onDeletedLayer(self, layer_id: str):
    if layer_id == _ROOT_LAYER_ID:
      self._root_layer = None
    else:
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
      self.last_passive_check_ms = time.ticks_ms()
      _thread.start_new_thread(_Connect_Threaded, (self._io,))

  def _checked_connect_threaded_async(self):
    global _ConnectThreadedResult
    if self._connected:
      return True
    now = time.ticks_ms()
    if now - self.last_passive_check_ms < _PASSIVE_CHECK_GAP_MS:
      return False
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
    self.last_passive_check_ms = time.ticks_ms()

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

  def _sendCommand(self, layer_id: str, command: str, *params, ack_seq: int = None):
    self._checkForFeedback()
    #self.switchDebugLed(True)
    try:
      if layer_id is not None:
        self._io.print(layer_id)
        if ack_seq is not None:
          self._io.print('@')
          self._io.print(_ACK_SEQ_TO_ACK_STR(ack_seq))
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

  def _sendBytesPortion(self, bytes_nature: str, bytes_data: bytes):
    self._checkForFeedback()
    byte_count = len(bytes_data)
    self._io.print('|bytes|>')
    if bytes_nature is not None:
      self._io.print(bytes_nature)
      self._io.print('#')
    self._io.print(str(byte_count))
    self._io.print(':')
    self._io.printBytes(bytes_data)

  def _sendBytesAfterCommand(self, bytes_data: bytes):
    self._sendBytesPortion(None, bytes_data)
    self._sendCommand(None, DDC_KAL)


  def _is_reconnecting(self) -> bool:
    if self._connected_iop is not None:
      return self._connected_iop.reconnecting
    else:
      return False

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
            #print(feedback)  # TODO: disable debug
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
          #print("** FEEDBACK: " + feedback)  # TODO: disable debug
          if idx != -1:
            try:
              lid = feedback[0:idx]
              feedback = feedback[idx + 1:]
              if feedback != "":
                idx = feedback.index(':')
                fb_type = feedback[0:idx]
                if len(fb_type) == 1 and fb_type >= "0" and fb_type <= "9":
                  x = int(fb_type)
                  y = 0
                  text = None
                  fb_type = "click"
                else:
                  if fb_type == "C":
                    fb_type = "click"
                  elif fb_type == "D":
                    fb_type = "doubleclick"
                  elif fb_type == "L":
                    fb_type = "longpress"
                  elif fb_type == "M":
                    fb_type = "move"
                  elif fb_type == "u":
                    fb_type = "up"
                  elif fb_type == "d":
                    fb_type = "down"
                  elif fb_type == "c":
                    fb_type = "custom"
                  feedback = feedback[idx + 1:]
                  idx = feedback.index(',')
                  idx2 = feedback.find(',', idx + 1)
                  x_str = feedback[0:idx]
                  if x_str != "":
                    x = int(x_str)
                  else:
                    x = 0
                  if idx2 == -1:
                    y_str = feedback[idx + 1:]
                    text = None
                  else:
                    y_str = feedback[idx + 1:idx2]
                    text = feedback[idx2 + 1:]
                  if y_str != "":
                    y = int(y_str)
                  else:
                    y = 0
              else:
                fb_type = "click"
                x = 0
                y = 0
                text = None
              layer = self._layers.get(lid)
              if layer is not None:
                if fb_type.startswith("_"):
                  ack_seq = fb_type[1:] if len(fb_type) > 1 else None
                  layer._handleAck(ack_seq, x, y, text)
                else:
                  layer._handleFeedback(fb_type, x, y)  # TODO: set text as feedback text
            except Exception as e:
              #print("** EXCEPT: " + feedback)
              if True:
                raise e
  def _readFeedback(self) -> str:
    validate_res = self._validateConnection()
    if validate_res is None:
      return None
    (need_reconnect, keep_alive_diff_ms) = validate_res
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
    else:
      return None
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
