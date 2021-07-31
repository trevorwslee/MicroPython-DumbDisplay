from _ddlayer import DDLayer
from _ddlayer import DD_BOOL_ARG

class LcdDDLayer(DDLayer):
  def __init__(self, dd, col_count = 16, row_count = 2, char_height = 0, font_name = ''):
    layer_id = dd._createLayer(str("lcd"), str(col_count), str(row_count), str(char_height), font_name)
    super().__init__(dd, layer_id)
  def print(self, text):
    self.dd._sendCommand(self.layer_id, "print", str(text))
  def home(self):
    self.dd._sendCommand(self.layer_id, "home")
  def setCursor(self, x, y):
    self.dd._sendCommand(self.layer_id, "setcursor", str(x), str(y))
  def cursor(self):
    self.dd._sendCommand(self.layer_id, "cursor", DD_BOOL_ARG(True))
  def noCursor(self):
    self.dd._sendCommand(self.layer_id, "cursor", DD_BOOL_ARG(False))
  def autoscroll(self):
    self.dd._sendCommand(self.layer_id, "autoscroll", DD_BOOL_ARG(True))
  def noAutoscroll(self):
    self.dd._sendCommand(self.layer_id, "autoscroll", DD_BOOL_ARG(False))
  def display(self):
    self.dd._sendCommand(self.layer_id, "display", DD_BOOL_ARG(True))
  def noDisplay(self):
    self.dd._sendCommand(self.layer_id, "display", DD_BOOL_ARG(False))
  def scrollDisplayLeft(self):
    self.dd._sendCommand(self.layer_id, "scrollleft")
  def scrollDisplayRight(self):
    self.dd._sendCommand(self.layer_id, "scrollright")
  def writeLine(self, text, y = 0, align = 'L'):
    self.dd._sendCommand(self.layer_id, "writeline", str(y), align, str(text))
  def writeCenteredLine(self, text, y = 0):
    self.dd._sendCommand(self.layer_id, "writeline", str(y), "C", str(text))
  def pixelColor(self, color):
    self.dd._sendCommand(self.layer_id, "pixelcolor", color)
  def bgPixelColor(self, color):
    self.dd._sendCommand(self.layer_id, "bgpixelcolor", color)
  def noBgPixelColor(self):
    self.dd._sendCommand(self.layer_id, "bgpixelcolor")




