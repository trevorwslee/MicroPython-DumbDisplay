

class _exp_DDTunnel():
  def __init__(self, dd, end_point) -> None:
      self.end_point = end_point
      self.dd = dd
      self.tunnel_id = dd._createTunnel(end_point)
      self._done = False
      self._data = []
      self.dd._onCreatedTunnel(self)
  def release(self):
    if not self._done:
      self.dd._sendSpecial("lt", self.tunnel_id, "disconnect")
    self._done = True
    self._data = None
    self.dd._onDeletedTunnel(self.tunnel_id)
    self.dd = None
  def reconnect(self):
    if self.dd is None:
      return False
    self.dd._reconnectTunnel(self.tunnel_id, self.end_point)
    self._done = False
    self._data = []
    return True
  def _count(self):
    return len(self._data) if self._data is not None else 0
  def _eof(self):
    return self._done and len(self._data) == 0
  def _readLine(self):
    if len(self._data) > 0:
      return self._data.pop(0)
    else:
      return None
  def _writeLine(self, line):
    self.dd._sendSpecial("lt", self.tunnel_id, None, line)

  def _handleInput(self, line, final):
    #print("HANDLEINPUT:" + str(line) + ":" + str(final))###
    if not final or line != "":
      self._data.append(line)
    if final:
      self._done = True
