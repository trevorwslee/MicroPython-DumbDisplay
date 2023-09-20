from ._ddlayer import DDLayer
from ._ddlayer import _DD_COLOR_ARG


class DDLayerLedGrid(DDLayer):
  '''Grid of LEDs'''
  def __init__(self, dd, col_count = 1, row_count = 1, sub_col_count = 1, sub_row_count = 1):
    '''
    :param dd: DumbDisplay object
    :param col_count: grid # columns
    :param row_count: grid # rows
    :param sub_col_count: # sub columns of each cell
    :param sub_row_count: # sub rows of each cell
    '''
    layer_id = dd._createLayer("ledgrid", str(col_count), str(row_count), str(sub_col_count), str(sub_row_count))
    super().__init__(dd, layer_id)
  def turnOn(self, x = 0, y = 0):
    '''turn on LED @ (x, y)'''
    self.dd._sendCommand(self.layer_id, "ledon", str(x), str(y))
  def turnOff(self, x = 0, y = 0):
    '''turn off LED @ (x, y)'''
    self.dd._sendCommand(self.layer_id, "ledoff", str(x), str(y))
  def toggle(self, x = 0, y = 0):
    '''toggle LED @ (x, y)'''
    self.dd._sendCommand(self.layer_id, "ledtoggle", str(x), str(y))
  def turnOnEx(self, x = 0, y = 0, onColor: str = ""):
    self.dd._sendCommand(self.layer_id, "ledonex", str(x), str(y), _DD_COLOR_ARG(onColor))
  def horizontalBar(self, count: int, rightToLeft = False):
    '''turn on LEDs to form a horizontal "bar"'''
    self.dd._sendCommand(self.layer_id, "ledhoribar", str(count), str(rightToLeft))
  def verticalBar(self, count: int, bottomToTop = True):
    '''turn on LEDs to form a vertical "bar"'''
    self.dd._sendCommand(self.layer_id, "ledvertbar", str(count), str(bottomToTop))
  def onColor(self, color):
    '''set LED on color'''
    self.dd._sendCommand(self.layer_id, "ledoncolor", _DD_COLOR_ARG(color))
  def offColor(self, color):
    '''set LED off color'''
    self.dd._sendCommand(self.layer_id, "ledoffcolor", _DD_COLOR_ARG(color))
  def noOffColor(self):
    '''/* set no LED off color */'''
    self.dd._sendCommand(self.layer_id, "ledoffcolor")
