#from ._ddlayer import DDLayer
from .ddimpl import DumbDisplayImpl
from .ddlayer_multilevel import DDLayerMultiLevel
from .ddlayer import _DD_COLOR_ARG, _DD_BOOL_ARG, _DD_INT_ARG


class DDLayerGraphicalBase(DDLayerMultiLevel):
  def __init__(self, dd: DumbDisplayImpl, layer_id: str):
    super().__init__(dd, layer_id)
  def setCursor(self, x, y):
    self.dd._sendCommand(self.layer_id, "setcursor", str(x), str(y))
  def moveCursorBy(self, by_x, by_y):
    self.dd._sendCommand(self.layer_id, "movecursorby", str(by_x), str(by_y))
  def setTextColor(self, color, bg_color = ""):
    """
    set the text color (i.e. pen color)
    :param bg_color: "" means default
    """
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
    """
    :param char: char to draw
    :param bg_color: "" means default
    :param size: 0 means defajult
    """
    self.dd._sendCommand(self.layer_id, "drawchar", str(x), str(y), _DD_COLOR_ARG(color), _DD_COLOR_ARG(bg_color), str(size), char)
  def drawStr(self, x, y, string, color, bg_color = "", size = 0):
    """
    :param bg_color: "" means default
    :param size: 0 means default
    """
    self.dd._sendCommand(self.layer_id, "drawstr", str(x), str(y), _DD_COLOR_ARG(color), _DD_COLOR_ARG(bg_color), str(size), string)
  def drawTextLine(self, text: str, y: int, align: str = "L", color: str = "", bgColor: str = "", size: int = 0):
    """
    similar to drawStr(), but draw string as a text line at (0, y) with alignment option
    :param align 'L', 'C', or 'R'
    """
    self.dd._sendCommand(self.layer_id, "drawtextline", _DD_INT_ARG(y), align, color, bgColor, _DD_INT_ARG(size), text)
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

  def drawImageFile(self, imageFileName: str, x: int = 0, y: int = 0, w: int = 0, h: int = 0, options = ""):
    """
    draw image file in cache (if not already loaded to cache, load it)
    :param x,y: position of the left-top corner
    :param w,h: image size to scale to; if both 0, will not scale, if any 0, will scale keeping aspect ratio
    """
    if x == 0 and y == 0 and w == 0 and h == 0:
      self.dd._sendCommand(self.layer_id, "drawimagefile", imageFileName, options)
    elif x == 0 and y == 0:
      if options == "":
        self.dd._sendCommand(self.layer_id, "drawimagefile", imageFileName, _DD_INT_ARG(w), _DD_INT_ARG(h))
      else:
        self.dd._sendCommand4(self.layer_id, "drawimagefile", imageFileName, _DD_INT_ARG(w), _DD_INT_ARG(h), options)
    else:
      if options == "":
        self.dd._sendCommand(self.layer_id, "drawimagefile", imageFileName, _DD_INT_ARG(x), _DD_INT_ARG(y), _DD_INT_ARG(w), _DD_INT_ARG(h))
      else:
        self.dd._sendCommand(self.layer_id, "drawimagefile", imageFileName, _DD_INT_ARG(x), _DD_INT_ARG(y), _DD_INT_ARG(w), _DD_INT_ARG(h), options)
  def drawImageFileFit(self, imageFileName: str, x: int = 0, y: int = 0, w: int = 0, h: int = 0, options: str = ""):
    """
    draw image file in cache (if not already loaded to cache, load it)
    :param x,y,w,h: rect to draw the image; 0 means the default value
    :param options (e.g. "LB"): left align "L"; right align "R"; top align "T"; bottom align "B"; default to fit centered
    """
    if x == 0 and y == 0 and w == 0 and h == 0 and options == "":
      self.dd._sendCommand(self.layer_id, "drawimagefilefit", imageFileName)
    else:
      self.dd._sendCommand(self.layer_id, "drawimagefilefit", imageFileName, _DD_INT_ARG(x), _DD_INT_ARG(y), _DD_INT_ARG(w), _DD_INT_ARG(h), options)
  def cacheImage(self, image_name: str, bytes_data: bytes):
    """
    cache image; not saved
    """
    self.dd._sendCommand(None, "CACHEIMG", self.layer_id, image_name)
    self.dd._sendBytesAfterCommand(bytes_data)

  def forward(self, distance):
    """draw forward relative to cursor position"""
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
    """draw polygon given side and vertex count"""
    self.dd._sendCommand(self.layer_id, "poly", str(side), str(vertex_count))
  def centeredPolygon(self, radius, vertex_count, inside = False):
    """
    draw polygon enclosed in an imaginary centered circle
    - given circle radius and vertex count
    - whether inside the imaginary circle or outside of it
    """
    self.dd._sendCommand(self.layer_id, "cpolyin" if inside else "cpoly", str(radius), str(vertex_count))
  def write(self, text, draw = False):
    """
    write text; will not auto wrap
    :param draw: draw means draw the text (honor the heading direction)
    """
    self.dd._sendCommand(self.layer_id, "drawtext" if draw else "write", text)


class DDLayerGraphical(DDLayerGraphicalBase):
  def __init__(self, dd: DumbDisplayImpl, width: int, height: int):
    """
    :param dd: DumbDisplay object
    :param width: width
    :param height: height
    """
    layer_id = dd._createLayer("graphical", _DD_INT_ARG(width), _DD_INT_ARG(height))
    super().__init__(dd, layer_id)


class DDRootLayer(DDLayerGraphicalBase):
  """
  it is [the only] root layer of the DumbDisplay, the foundation layer on which all other layers are contained;
  it is basically a graphical layer, but without feedback capability
  """
  def __init__(self, dd: DumbDisplayImpl, width: int, height: int, contained_alignment: str = ""):
    """
    set the root layer of the DumbDisplay; it is basically a graphical layer
    :param dd: DumbDisplay object
    :param width: width
    :param height: height
    """
    layer_id = dd._setRootLayer(width, height, contained_alignment)
    super().__init__(dd, layer_id)
