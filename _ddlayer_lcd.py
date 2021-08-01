from _ddlayer import DDLayer
from _ddlayer import _DD_BOOL_ARG
from _ddlayer import _DD_COLOR_ARG

class DDLayerLcd(DDLayer):
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
    self.dd._sendCommand(self.layer_id, "cursor", _DD_BOOL_ARG(True))
  def noCursor(self):
    self.dd._sendCommand(self.layer_id, "cursor", _DD_BOOL_ARG(False))
  def autoscroll(self):
    self.dd._sendCommand(self.layer_id, "autoscroll", _DD_BOOL_ARG(True))
  def noAutoscroll(self):
    self.dd._sendCommand(self.layer_id, "autoscroll", _DD_BOOL_ARG(False))
  def display(self):
    self.dd._sendCommand(self.layer_id, "display", _DD_BOOL_ARG(True))
  def noDisplay(self):
    self.dd._sendCommand(self.layer_id, "display", _DD_BOOL_ARG(False))
  def scrollDisplayLeft(self):
    self.dd._sendCommand(self.layer_id, "scrollleft")
  def scrollDisplayRight(self):
    self.dd._sendCommand(self.layer_id, "scrollright")
  def writeLine(self, text, y = 0, align = "L"):
    '''write text as a line, with alignment "L", "C", or "R"'''
    self.dd._sendCommand(self.layer_id, "writeline", str(y), align, str(text))
  def writeCenteredLine(self, text, y = 0):
    '''write text as a line, with align "centered"'''
    self.dd._sendCommand(self.layer_id, "writeline", str(y), "C", str(text))
  def pixelColor(self, color):
    '''set pixel color'''
    self.dd._sendCommand(self.layer_id, "pixelcolor", _DD_COLOR_ARG(color))
  def bgPixelColor(self, color):
    '''set "background" (off) pixel color'''
    self.dd._sendCommand(self.layer_id, "bgpixelcolor", _DD_COLOR_ARG(color))
  def noBgPixelColor(self):
    '''set no "background" (off) pixel color'''
    self.dd._sendCommand(self.layer_id, "bgpixelcolor")




