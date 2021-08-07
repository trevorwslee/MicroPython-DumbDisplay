from _ddlayer import DDLayer
from _ddlayer import _DD_COLOR_ARG
from _ddlayer import _DD_BOOL_ARG

class DDLayerGraphical(DDLayer):
  '''Graphical LCD'''
  def __init__(self, dd, width, height):
    '''
    :param dd: DumbDisplay object
    :param width: width
    :param height: height
    '''
    layer_id = dd._createLayer(str("graphical"), str(width), str(height))
    super().__init__(dd, layer_id)
  def setCursor(self, x, y):
    self.dd._sendCommand(self.layer_id, "setcursor", str(x), str(y))
  def moveCursor(self, by_x, by_y):
    self.dd._sendCommand(self.layer_id, "movecursorby", str(by_x), str(by_y))
  def setTextColor(self, color, bg_color = ""):
    self.dd._sendCommand(self.layer_id, "textcolor", _DD_COLOR_ARG(color), _DD_COLOR_ARG(bg_color))
  def setTextSize(self, size):
    self.dd._sendCommand(self.layer_id, "textsize", str(size))
  def setTextFont(self, font_name, size):
    self.dd._sendCommand(self.layer_id, "textfont", font_name, str(size))
  def setTextWrap(self, wrap_on):
    self.dd._sendCommand(self.layer_id, "settextwrap", _DD_BOOL_ARG(wrap_on))
