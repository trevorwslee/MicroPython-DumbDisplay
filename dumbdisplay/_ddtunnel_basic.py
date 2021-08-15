from ._ddtunnel import DDTunnel


class DDBasicTunnel(DDTunnel):
  def __init__(self, dd, end_point) -> None:
    tunnel_id = dd._createTunnel(end_point)
    super().__init__(dd, tunnel_id)
  def count(self):
    return self._count()
  def eof(self):
    return self._eof()
  def readLine(self):
    return self._readLine()
  def writeLine(self, line):
    return self._writeLine(line)
