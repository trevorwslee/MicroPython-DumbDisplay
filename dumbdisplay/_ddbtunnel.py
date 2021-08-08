

class DDTunnel():
  def __init__(self, dd, end_point) -> None:
      self.dd = dd
      self.tunnel_id = self.dd._lt_createTunnel(end_point)
      self._next_data = None
      self._buffer = []
      self.dd._lt_onCreatedTunnel(self)
  def avail(self):
    if self.dd == None:
      raise RuntimeError("not opened") 
    if self._next_data == None:  
      self._next_data = self.dd_lt_read(self)
    if self._next_data != None:
      return len(self._next_data)
    else:
      return 0     
  def read(self):
    if self.dd == None:
      raise RuntimeError("not opened")
    if self._next_data != None:
      return self._next_data
    else:
      return self.dd._lt_read(self)
  def write(self, data):
    if self.dd == None:
      raise RuntimeError("not opened")
    self.dd._lt_send(self.tunnel_id, data)
  def release(self):
    self.dd._lt_onDeletedTunnel(self)
    self.dd = None
