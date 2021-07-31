
def DD_BOOL_ARG(b):
  if b:
    return "1"
  else:
    return "0"


class DDLayer:
  def __init__(self, dd, layer_id):
    self.dd = dd
    self.layer_id = layer_id
  def visibility(self, visible):
    '''set layer visibility'''
    self.dd._sendCommand(self.layer_id, "visible", str(visible))
  def opacity(self, opacity):
    '''set layer opacity -- 0 to 255'''
    self.dd._sendCommand(self.layer_id, "opacity", str(opacity))
  def border(self, size, color, shape):
    '''
    :param size: unit is pixel
                  - LcdLayer; each character is composed of pixels
                  - 7SegmentRowLayer; each 7-segment is composed of fixed 220 x 320 pixels
                  - LedGridLayer; a LED is considered as a pixel
    :param shape: can be "flat", "round", "raised" or "sunken"
    '''
    self.dd._sendCommand(self.layer_id, "border", str(size), color, shape)
  def padding(self, left, top, right, bottom):
    '''see border() for size unit'''
    self.dd._sendCommand(self.layer_id, "padding", str(left), str(top), str(right), str(bottom))
  def noPadding(self):
    self.dd._sendCommand(self.layer_id, "padding")
  def backgroundColor(self, color):
    self.dd._sendCommand(self.layer_id, "bgcolor", color)
  def noBackgroundColor(self):
    self.dd._sendCommand(self.layer_id, "nobgcolor")
  def clear(self):
    '''clear the layer'''
    self.dd._sendCommand(self.layer_id, "clear")
  def flash(self):
    self.dd._sendCommand(self.layer_id, "flash")
  def flashArea(self, x, y):
    self.dd._sendCommand(self.layer_id, "flasharea", str(x), str(y));
  def writeComment(self, comment):
    self.dd.writeComment(comment)
  def release(self):
    self.dd._deleteLayer(self.layer_id)


