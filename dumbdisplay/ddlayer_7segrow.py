from .ddimpl import DumbDisplayImpl
from .ddlayer import DDLayer
from .ddlayer import _DD_COLOR_ARG

class DDLayer7SegmentRow(DDLayer):
  '''A row of 7 Segments'''
  def __init__(self, dd: DumbDisplayImpl, digit_count = 1):
    '''
    :param dd: DumbDisplay object
    :param digit_count: number of digits / # rows
    '''
    layer_id = dd._createLayer("7segrow", str(digit_count))
    super().__init__(dd, layer_id)
  def segmentColor(self, color):
    '''set segment color'''
    self.dd._sendCommand(self.layer_id, "segcolor", _DD_COLOR_ARG(color))
  def turnOn(self, segments, digit_idx = 0):
    '''
    turn on one or more segments
    :param segments: each character represents a segment to turn off
                     - 'a', 'b', 'c', 'd', 'e', 'f', 'g', '.'
    '''
    self.dd._sendCommand(self.layer_id, "segon", segments, str(digit_idx))
  def turnOff(self, segments, digit_idx = 0):
    '''turn off one or more segments -- see turnOn()'''
    self.dd._sendCommand(self.layer_id, "segoff", segments, str(digit_idx))
  def setOn(self, segments = "", digit_idx = 0):
    '''like turnOn(), exception that the digit will be cleared first;'''
    '''empty segments basically means turn all segments of the digit off'''
    self.dd._sendCommand(self.layer_id, "setsegon", segments, str(digit_idx))
  def showDigit(self, digit: int, digit_idx: int = 0):
     '''
     show a digit
     '''
     self.dd._sendCommand(self.layer_id, "showdigit", str(digit) , str(digit_idx))
  def showNumber(self, number):
    '''show number'''
    self.dd._sendCommand(self.layer_id, "shownumber", str(number))
  def showHexNumber(self, number):
    '''show HEX number'''
    self.dd._sendCommand(self.layer_id, "showhex", str(number))
  def showFormatted(self, formatted):
    '''
     show formatted number (even number with hex digits)
     -- e.g. "12.00", "00.34", "-.12", "0ff"
    '''
    self.dd._sendCommand(self.layer_id, "showformatted", str(formatted))




