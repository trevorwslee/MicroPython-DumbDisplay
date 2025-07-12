
def DD_RGB_COLOR(r: int, g: int, b: int):
  return r * 0x10000 + g * 0x100 + b

def _DD_INT_ARG(val: int):
  return str(int(val))


def _DD_FLOAT_IS_ZERO(val: float) -> bool:
  return val >= -0.001 and val <= 0.001

def _DD_FLOAT_IS_WHOLE(val: float) -> bool:
  delta = val - int(val)
  return delta >= -0.001 and delta <= 0.001

def _DD_FLOAT_ARG(val: float):
  if True:
    #since 2025-07-09 .., if very close to int, use int
    # delta = val - int(val)
    # if delta >= -0.001 and delta <= 0.001:
    #   return str(int(val))
    if _DD_FLOAT_IS_WHOLE(val):
      return str(int(val))
  return str(float(val))

def _DD_BOOL_ARG(b: bool):
  if b:
    return "1"
  else:
    return "0"

def _DD_COLOR_ARG(c):
  if type(c) is int:
    return '#' + hex(c)[2:]
  else:
    return str(c)



class DDFeedback:
  '''
  type: can be "click", "doubleclick", "longpress"
  '''
  def __init__(self, type, x, y):
    self.type = type
    self.x = x
    self.y = y

class DDLayer:
  def __init__(self, dd, layer_id):
    self.dd = dd
    self.layer_id = layer_id
    self._feedback_handler = None
    self._feedbacks = []
    #self.customData = ""
    dd._onCreatedLayer(self)
  def visibility(self, visible: bool):
    '''set layer visibility'''
    self.dd._sendCommand(self.layer_id, "visible", _DD_BOOL_ARG(visible))
  def disabled(self, disabled: bool = True):
    '''set layer disabled'''
    self.dd._sendCommand(self.layer_id, "disabled", _DD_BOOL_ARG(disabled))
  def transparent(self, transparent: bool):
    self.dd._sendCommand(self.layer_id, "transparent", _DD_BOOL_ARG(transparent))
  def opacity(self, opacity: int):
    '''set layer opacity percentage -- 0 to 100'''
    self.dd._sendCommand(self.layer_id, "opacity", str(opacity))
  def alpha(self, alpha: int):
    '''set layer alpha -- 0 to 255'''
    self.dd._sendCommand(self.layer_id, "alpha", str(alpha))
  def border(self, size, color, shape: str = "flat", extra_size = 0):
    '''
    :param size: unit is pixel
                  - LcdLayer; each character is composed of pixels
                  - 7SegmentRowLayer; each 7-segment is composed of fixed 220 x 320 pixels
                  - LedGridLayer; a LED is considered as a pixel
    :param shape: can be "flat", "round", "raised" or "sunken"
    :param extra_size just added to size; however if shape is "round", it affects the "roundness"
    '''
    if type(extra_size) == int and extra_size == 0:
      self.dd._sendCommand(self.layer_id, "border", str(size), _DD_COLOR_ARG(color), shape)
    else:
      self.dd._sendCommand(self.layer_id, "border", str(size), _DD_COLOR_ARG(color), shape, str(extra_size))
  def noBorder(self):
    self.dd._sendCommand(self.layer_id, "border")
  def padding(self, left, top = None, right = None, bottom = None):
    '''see border() for size unit'''
    if top is None and right is None and bottom is None:
      self.dd._sendCommand(self.layer_id, "padding", str(left))
    else:
      if top is None:
        top = left
      if right is None:
        right = left
      if bottom is None:
        bottom = top
      self.dd._sendCommand(self.layer_id, "padding", str(left), str(top), str(right), str(bottom))
  def noPadding(self):
    self.dd._sendCommand(self.layer_id, "padding")
  def margin(self, left, top = None, right = None, bottom = None):
    '''see border() for size unit'''
    if top is None and right is None and bottom is None:
      self.dd._sendCommand(self.layer_id, "margin", str(left))
    else:
      if top is None:
        top = left
      if right is None:
        right = left
      if bottom is None:
        bottom = top
      self.dd._sendCommand(self.layer_id, "margin", str(left), str(top), str(right), str(bottom))
  def noMargin(self):
    self.dd._sendCommand(self.layer_id, "margin")
  def backgroundColor(self, color, opacity = 100):
    '''
    :param opacity: background opacity (0 - 100)
    :return:
    '''
    if opacity < 100:
      self.dd._sendCommand(self.layer_id, "bgcolor", _DD_COLOR_ARG(color), str(opacity))
    else:
      self.dd._sendCommand(self.layer_id, "bgcolor", _DD_COLOR_ARG(color))
  def noBackgroundColor(self):
    self.dd._sendCommand(self.layer_id, "nobgcolor")
  def clear(self):
    '''clear the layer'''
    self.dd._sendCommand(self.layer_id, "clear")
  def flash(self):
    self.dd._sendCommand(self.layer_id, "flash")
  def flashArea(self, x, y):
    self.dd._sendCommand(self.layer_id, "flasharea", str(x), str(y))
  # def writeComment(self, comment):
  #   self.dd.writeComment(comment)
  def enableFeedback(self, auto_feedback_method = "", feedback_handler = None, allowed_feedback_types = ""):
    '''
    rely on getFeedback() being called */
    :param auto_feedback_method:
    . "" -- no auto feedback
    . "f" -- flash the default way (layer + border)
    . "fl" -- flash the layer
    . "fa" -- flash the area where the layer is clicked
    . "fas" -- flash the area (as a spot) where the layer is clicked
    . "fs" -- flash the spot where the layer is clicked (regardless of any area boundary)
    :param feedback_handler: function that accepts (layer, type, x, y) as parameters
    . layer -- layer involved
    . type -- "click"
    . x, y -- the "area" on the layer where was clicked
    '''
    self._feedback_handler = feedback_handler
    self._feedbacks = []
    self.dd._sendCommand(self.layer_id, "feedback", _DD_BOOL_ARG(True), auto_feedback_method, allowed_feedback_types)
  def disableFeedback(self):
    '''disable feedback'''
    self.dd._sendCommand(self.layer_id, "feedback", _DD_BOOL_ARG(False))
    self._feedback_handler = None
  def getFeedback(self) -> DDFeedback:
    '''
    get any feedback as the structure {type, x, y}
    :return: None if none (or when "handler" set)
    '''
    self.dd._checkForFeedback()
    if len(self._feedbacks) > 0:
      (type, x, y) = self._feedbacks.pop(0)
      return DDFeedback(type, x, y)
    else:
      return None
  # def setFeedbackHandler(self, feedback_handler):
  #   self._feedback_handler = feedback_handler
  #   self._shipFeedbacks()
  def reorder(self, how: str):
    '''
     recorder the layer
     :param how: can be "T" for top; or "B" for bottom; "U" for up; or "D" for down
    '''
    self.dd._reorderLayer(self.layer_id, how)
  def release(self):
    '''release the layer'''
    self.dd._deleteLayer(self.layer_id)
    self.dd._onDeletedLayer(self.layer_id)
    self.dd = None
  def pinLayer(self, uLeft: int, uTop: int, uWidth: int, uHeight: int, align: str = ""):
    self.dd._pinLayer(self.layer_id, uLeft, uTop, uWidth, uHeight, align)
  def reorderLayer(self, how: str):
    self.dd._reorderLayer(self.layer_id, how)


  def _handleFeedback(self, type, x, y):
    #print("RAW FB: " + self.layer_id + '.' + type + ':' + str(x) + ',' + str(y))
    if self._feedback_handler is not None:
      self._feedback_handler(self, type, x, y)
    else:
      self._feedbacks.append((type, x, y))
      # self._shipFeedbacks()



