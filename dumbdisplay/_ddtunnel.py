

class DDTunnel():
  def __init__(self, dd, tunnel_id) -> None:
      self.dd = dd
      self.tunnel_id = tunnel_id
      self._done = False
      self._data = []
      self.dd._onCreatedTunnel(self)
  def release(self):
    if not self.done:
      self.dd._sendSpecial("lt", self.tunnel_id, "disconnect")
    self._done = True
    self._data = None
    self.dd._onDeletedTunnel()
    self.dd = None
  def _count(self):
    return len(self._data) if self._data != None else 0
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
    if not final or line != "":
      self._data.append(line)
    if final:
      self._done = True
