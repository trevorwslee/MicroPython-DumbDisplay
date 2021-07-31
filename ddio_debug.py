from ddio import DDInputOutput

class DDDebugIO(DDInputOutput):
  def __init__(self):
    self.values = ["ddhello\n", "<init<:999\n"]
    self.idx = 0
    self.value_idx = 0
  def available(self):
    return self.idx < len(self.values)
  def read(self):
    value = self.values[self.idx] 
    c = value[self.value_idx: self.value_idx + 1] 
    self.value_idx += 1
    if self.value_idx >= len(value):
      self.value_idx = 0
      self.idx += 1
    return c
  def print(self, s):
    print(s)
