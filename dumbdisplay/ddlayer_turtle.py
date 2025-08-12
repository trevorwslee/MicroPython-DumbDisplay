#from ._ddlayer import DDLayer
from .ddlayer_multilevel import DDLayer
from .ddlayer import _DD_COLOR_ARG, _DD_BOOL_ARG, _DD_INT_ARG

class DDLayerTurtle(DDLayer):
  '''Turtle-like Layer'''
  def __init__(self, dd, width, height):
    '''
    :param dd: DumbDisplay object
    :param width: width
    :param height: height
    '''
    self._init(dd, width, height, track_move=False)
  def _init(self, dd, width, height, track_move: bool):
    if track_move:
      layer_id = dd._createLayer("turtle", _DD_INT_ARG(width), _DD_INT_ARG(height), _DD_BOOL_ARG(True))
    else:
      layer_id = dd._createLayer("turtle", _DD_INT_ARG(width), _DD_INT_ARG(height))
    super().__init__(dd, layer_id)
  def forward(self, distance: int, with_pen: bool = True):
    '''
    forward; with pen or not
    '''
    self._sendCommandToDD("fd" if with_pen else "jfd", _DD_INT_ARG(distance))
  def backward(self, distance: int, with_pen: bool = True):
    '''
    backward; with pen or not
    '''
    self._sendCommandToDD("bk" if with_pen else "jbk", _DD_INT_ARG(distance))
  def leftTurn(self,  angle: int):
    '''
    left turn
    '''
    self.dd._sendCommand(self.layer_id, "lt", _DD_INT_ARG(angle))
  def rightTurn(self, angle: int):
    '''
    right turn
    '''
    self.dd._sendCommand(self.layer_id, "rt", _DD_INT_ARG(angle))
  def home(self, with_pen: bool = True):
    '''
    go home (0, 0); with pen or not
    '''
    self._sendCommandToDD("home" if with_pen else "jhome")
  def goTo(self, x: int, y: int, with_pen: bool = True):
    '''
    go to (x, y); with pen or not
    '''
    self._sendCommandToDD("goto" if with_pen else "jto", _DD_INT_ARG(x), _DD_INT_ARG(y))
  def goBy(self, by_x: int, by_y: int, with_pen: bool = True):
    '''
    go by (by_x, by_y); with pen or not
    '''
    self._sendCommandToDD("goby" if with_pen else "jby", _DD_INT_ARG(by_x), _DD_INT_ARG(by_y))
  def setHeading(self, angle: int):
    '''
    set heading angle (degree)
    '''
    self.dd._sendCommand(self.layer_id, "seth", _DD_INT_ARG(angle))
  def penSize(self, size: int):
    '''
    set pen size
    '''
    self.dd._sendCommand(self.layer_id, "pensize", _DD_INT_ARG(size))
  def penColor(self, color: str):
    '''
    set pen color
    '''
    self.dd._sendCommand(self.layer_id, "pencolor", _DD_COLOR_ARG(color))
  def fillColor(self, color: str):
    '''
    set fill color
    '''
    self.dd._sendCommand(self.layer_id, "fillcolor", _DD_COLOR_ARG(color))
  def noColor(self):
    '''
    set no fill color
    '''
    self.dd._sendCommand(self.layer_id, "nofillcolor")
  def penFilled(self, filled: bool = True):
    '''
    set pen filled or not
    '''
    self.dd._sendCommand(self.layer_id, "pfilled", _DD_BOOL_ARG(filled))
  def setTextSize(self, size: int):
    '''
    set text size
    '''
    self.dd._sendCommand(self.layer_id, "ptextsize", _DD_INT_ARG(size))
  def setTextFont(self, font_name = "", text_size = 0):
    '''
    set font
    @param font_name: empty means default
    @param text_size: 0 means default
    '''
    self.dd._sendCommand(self.layer_id, "ptextfont", font_name, _DD_INT_ARG(text_size))
  def penUp(self):
    '''pen up'''
    self.dd._sendCommand(self.layer_id, "pu")
  def penDown(self):
    '''pen down'''
    self.dd._sendCommand(self.layer_id, "pd")
  def beginFill(self):
    '''begin fill'''
    self.dd._sendCommand(self.layer_id, "begin_fill")
  def endFill(self):
    '''end fill'''
    self.dd._sendCommand(self.layer_id, "end_fill")
  def dot(self, size: int, color: str):
    '''draw a dot'''
    self._sendCommandToDD("dot", _DD_INT_ARG(size), _DD_COLOR_ARG(color))
  def circle(self, radius: int, centered: bool = False):
    """draw circle; centered or not"""
    self._sendCommandToDD("ccircle" if centered else "circle", _DD_INT_ARG(radius))
  def oval(self, width: int, height: int, centered: bool = False):
    """draw oval; centered or not"""
    self._sendCommandToDD("coval" if centered else "oval", _DD_INT_ARG(width), _DD_INT_ARG(height))
  def arc(self, width: int, height: int, start_angle: int, sweep_angle: int, centered: bool = False):
    """draw arc; centered or not"""
    self._sendCommandToDD("carc" if centered else "arc", _DD_INT_ARG(width), _DD_INT_ARG(height), _DD_INT_ARG(start_angle), _DD_INT_ARG(sweep_angle))
  def triangle(self, side1: int, angle: int, side2: int):
    """draw triangle (SAS)"""
    self._sendCommandToDD("trisas", _DD_INT_ARG(side1), _DD_INT_ARG(angle), _DD_INT_ARG(side2))
  def isoscelesTriangle(self, side: int, angle: int):
    """draw isosceles triangle; given size and angle"""
    self._sendCommandToDD("trisas", _DD_INT_ARG(side), _DD_INT_ARG(angle))
  def rectangle(self, width: int, height: int, centered: bool = False):
    """draw rectangle; centered or not"""
    self._sendCommandToDD("crect" if centered else "rect", _DD_INT_ARG(width), _DD_INT_ARG(height))
  def polygon(self, side: int, vertex_count: int):
    """draw polygon given side and vertex count"""
    self._sendCommandToDD("poly", _DD_INT_ARG(side), _DD_INT_ARG(vertex_count))
  def centeredPolygon(self, radius: int, vertex_count: int, inside: bool = False):
    """draw polygon enclosed in an imaginary centered circle
    - given circle radius and vertex count
    - whether inside the imaginary circle or outside of it"""
    self._sendCommandToDD("cpolyin" if inside else "cpoly", _DD_INT_ARG(radius), _DD_INT_ARG(vertex_count))
  def write(self, text: str, draw: bool = False):
    """write text; draw means draw the text (honor heading)"""
    self._sendCommandToDD("drawtext" if draw else "write", text)
  def _sendCommandToDD(self, command: str, *params):
    self.dd._sendCommand(self.layer_id, command, *params)


class DDLayerTurtleTracked(DDLayerTurtle):  # TODO: working on DDLayerTurtleTracked
  '''Graphical LCD'''
  def __init__(self, dd, width, height):
    '''
    :param dd: DumbDisplay object
    :param width: width
    :param height: height
    '''
    self._init(dd, width, height, track_move=True)
    self._x: int = 0
    self._y: int = 0
  def pos(self) -> (int, int):
    self.dd.timeslice()
    return (self._x, self._y)
  def xcor(self) -> int:
    self.dd.timeslice()
    return self._x
  def ycor(self) -> int:
    self.dd.timeslice()
    return self._y
  def _sendCommandToDD(self, command: str, *params):
    self.dd._sendCommand(self.layer_id, command, *params, ack_seq="0")  # TODO: make use of ack_seq
  def _handleAck(self, x, y, ack_seq: str):
    self._x = x
    self._y = y
