from ._ddlayer import DDLayer
from ._ddlayer import _DD_COLOR_ARG
from ._ddlayer import _DD_BOOL_ARG

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
    '''
    set the text color (i.e. pen color)
    :param bg_color: "" means means default
    '''
    self.dd._sendCommand(self.layer_id, "textcolor", _DD_COLOR_ARG(color), _DD_COLOR_ARG(bg_color))
  def setTextSize(self, size):
    self.dd._sendCommand(self.layer_id, "textsize", str(size))
  def setTextFont(self, font_name, size = 0):
    """
    :param size: 0 means default size
    """
    self.dd._sendCommand(self.layer_id, "textfont", font_name, str(size))
  def setTextWrap(self, wrap_on):
    self.dd._sendCommand(self.layer_id, "settextwrap", _DD_BOOL_ARG(wrap_on))
  def print(self, text):
    self.dd._sendCommand(self.layer_id, "print", text)
  def println(self, text = ""):
    self.dd._sendCommand(self.layer_id, "println", text)
  def fillScreen(self, color):
    self.dd._sendCommand(self.layer_id, "fillscreen", _DD_COLOR_ARG(color))
  def drawChar(self, x, y, char, color, bg_color = "", size = 0):
    '''
    :param char: char to draw
    :param bg_color: "" means default
    :param size: 0 means defajult
    '''
    self.dd._sendCommand(self.layer_id, "drawchar", str(x), str(y), _DD_COLOR_ARG(color), _DD_COLOR_ARG(bg_color), str(size), char)
  def drawText(self, x, y, text, color, bg_color = "", size = 0):
    '''
    :param bg_color: "" means default
    :param size: 0 means defajult
    '''
    self.dd._sendCommand(self.layer_id, "drawtext", str(x), str(y), _DD_COLOR_ARG(color), _DD_COLOR_ARG(bg_color), str(size), text)
  def drawPixel(self, x, y, color):
    self.dd._sendCommand(self.layer_id, "drawpixel", str(x), str(y), _DD_COLOR_ARG(color))
  def drawLine(self, x1, y1, x2, y2, color):
    self.dd._sendCommand(self.layer_id, "drawline", str(x1), str(y1), str(x2), str(y2), _DD_COLOR_ARG(color))
  def drawRect(self, x, y, w, h, color, filled = False):
    self.dd._sendCommand(self.layer_id, "drawrect", str(x), str(y), str(w), str(h), _DD_COLOR_ARG(color), _DD_BOOL_ARG(filled))
  def drawCircle(self, x, y, r, color, filled = False):
    self.dd._sendCommand(self.layer_id, "drawcircle", str(x), str(y), str(r), _DD_COLOR_ARG(color), _DD_BOOL_ARG(filled))
  def drawTriangle(self, x1, y1, x2, y2, x3, y3, color, filled = False):
    self.dd._sendCommand(self.layer_id, "drawtriangle", str(x1), str(y1), str(x2), str(y2), str(x3), str(y3), _DD_COLOR_ARG(color), _DD_BOOL_ARG(filled))
  def drawRoundRect(self, x, y, w, h, r, color, filled = False):
    self.dd._sendCommand(self.layer_id, "drawroundrect", str(x), str(y), str(w), str(h), str(r), _DD_COLOR_ARG(color), _DD_BOOL_ARG(filled))

  def forward(self, distance):
    '''draw forward relative to cursor position'''
    self.dd._sendCommand(self.layer_id, "fd", str(distance))
  def leftTurn(self, angle):
    self.dd._sendCommand(self.layer_id, "lt", str(angle))
  def rightTurn(self, angle):
    self.dd._sendCommand(self.layer_id, "rt", str(angle))
  def setHeading(self, angle):
    self.dd._sendCommand(self.layer_id, "seth", str(angle))
  def penSize(self, size):
    self.dd._sendCommand(self.layer_id, "pensize", str(size))
  def penColor(self, color):
    self.dd._sendCommand(self.layer_id, "pencolor", _DD_COLOR_ARG(color))
  def fillColor(self, color):
    self.dd._sendCommand(self.layer_id, "fillcolor", _DD_COLOR_ARG(color))
  def noFillColor(self):
    self.dd._sendCommand(self.layer_id, "nofillcolor")
  def circle(self, radius, centered = False):
    self.dd._sendCommand(self.layer_id, "ccircle" if centered else "circle", str(radius))
  def oval(self, width, height, centered = False):
    self.dd._sendCommand(self.layer_id, "coval" if centered else "oval", str(width), str(height))
  def rectangle(self, width, height, centered = False):
    self.dd._sendCommand(self.layer_id, "crect" if centered else "rect", str(width), str(height))
  def triangle(self, side1, angle, side2):
    self.dd._sendCommand(self.layer_id, "trisas", str(side1), str(angle), str(side2))
  def isoscelesTriangle(self, side, angle):
    self.dd._sendCommand(self.layer_id, "trisas", str(side), str(angle))
  def polygon(self, side, vertex_count):
    '''draw polygon given side and vertex count'''
    self.dd._sendCommand(self.layer_id, "poly", str(side), str(vertex_count))
  def centeredPolygon(self, radius, vertex_count, inside = False):
    '''
    draw polygon enclosed in an imaginary centered circle
    - given circle radius and vertex count
    - whether inside the imaginary circle or outside of it
    '''
    self.dd._sendCommand(self.layer_id, "cpolyin" if inside else "cpoly", str(radius), str(vertex_count))
  def write(self, text, draw = False):
    '''
    write text; will not auto wrap
    :param draw: draw means draw the text (honor the heading direction)
    '''
    self.dd._sendCommand(self.layer_id, "drawtext" if draw else "write", text)


