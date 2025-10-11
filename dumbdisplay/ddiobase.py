DD_DEF_PORT = 10201

class DDInputOutput:
  def __init__(self):
    pass
  def preconnect(self):
    pass
  def available(self) -> bool:
    pass
  def read(self) -> str:
    pass
  def print(self, s: str):
    pass
  def printBytes(self, bytes_data: bytes):
    raise NotImplementedError("printBytes() not implemented")
  def close(self):
    pass


