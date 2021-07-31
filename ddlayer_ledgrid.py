from ddlayer import DDLayer


class LedGridDDLayer(DDLayer):
  def __init__(self, dd, col_count = 1, row_count = 1, sub_col_count = 1, sub_row_count = 1):
    layer_id = dd._createLayer(str("ledgrid"), str(col_count), str(row_count), str(sub_col_count), str(sub_row_count))
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
  def horizontalBar(self, count, rightToLeft = False):
    '''turn on LEDs to form a horizontal "bar"'''
    self.dd._sendCommand(self.layer_id, "ledhoribar", str(count), str(rightToLeft))
  def verticalBar(self, count, bottomToTop = True):
    '''turn on LEDs to form a vertical "bar"'''
    self.dd._sendCommand(self.layer_id, "ledvertbar", str(count), str(bottomToTop))
  def onColor(self, color):
    '''set LED on color'''
    self.dd._sendCommand(self.layer_id, "ledoncolor", color)
  def offColor(self, color):
    '''set LED off color'''
    self.dd._sendCommand(self.layer_id, "ledoffcolor", color)
  def noOffColor(self):
    '''/* set no LED off color */'''
    self.dd._sendCommand(self.layer_id, "ledoffcolor")
