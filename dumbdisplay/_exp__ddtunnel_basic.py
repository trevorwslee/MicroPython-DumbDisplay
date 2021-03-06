from ._exp__ddtunnel import _exp_DDTunnel


class _exp_DDBasicTunnel(_exp_DDTunnel):
  '''tunnel is ONLY supported with DumbDisplayWifiBridge -- https://www.youtube.com/watch?v=0UhRmXXBQi8'''
  def __init__(self, dd, end_point) -> None:
    super().__init__(dd, end_point)
#    tunnel_id = dd._createTunnel(end_point)
#    super().__init__(dd, tunnel_id)
  def count(self):
    return self._count()
  def eof(self):
    return self._eof()
  def readLine(self):
    return self._readLine()
  def writeLine(self, line):
    return self._writeLine(line)
