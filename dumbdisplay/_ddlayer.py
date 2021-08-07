

def _DD_BOOL_ARG(b):
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
    dd._onCreatedLayer(self)
  def visibility(self, visible):
    '''set layer visibility'''
    self.dd._sendCommand(self.layer_id, "visible", _DD_BOOL_ARG(visible))
  def opacity(self, opacity):
    '''set layer opacity -- 0 to 255'''
    self.dd._sendCommand(self.layer_id, "opacity", str(opacity))
  def border(self, size, color, shape = "flat"):
    '''
    :param size: unit is pixel
                  - LcdLayer; each character is composed of pixels
                  - 7SegmentRowLayer; each 7-segment is composed of fixed 220 x 320 pixels
                  - LedGridLayer; a LED is considered as a pixel
    :param shape: can be "flat", "round", "raised" or "sunken"
    '''
    self.dd._sendCommand(self.layer_id, "border", str(size), _DD_COLOR_ARG(color), shape)
  def noBorder(self):
    self.dd._sendCommand(self.layer_id, "border")
  def padding(self, left, top, right, bottom):
    '''see border() for size unit'''
    self.dd._sendCommand(self.layer_id, "padding", str(left), str(top), str(right), str(bottom))
  def noPadding(self):
    self.dd._sendCommand(self.layer_id, "padding")
  def backgroundColor(self, color):
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
  def writeComment(self, comment):
    self.dd.writeComment(comment)
  def enableFeedback(self, auto_feedback_method = "fa", feedback_handler = None):
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
    self.dd._sendCommand(self.layer_id, "feedback", _DD_BOOL_ARG(True), auto_feedback_method)
  def disableFeedback(self):
    '''disable feedback'''
    self.dd._sendCommand(self.layer_id, "feedback", _DD_BOOL_ARG(False))
    self._feedback_handler = None
  def getFeedback(self):
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
  def release(self):
    self.dd._deleteLayer(self.layer_id)
    self.dd._onDeletedLayer(self)


  def _handleFeedback(self, type, x, y):
    #print("RAW FB: " + self.layer_id + '.' + type + ':' + str(x) + ',' + str(y))
    if self._feedback_handler != None:
      self._feedback_handler(self, type, x, y)
    else:
      self._feedbacks.append((type, x, y))
      # self._shipFeedbacks()
  # def _shipFeedbacks(self):
  #   if self._feedback_handler != None:
  #     feedbacks = self._feedbacks.copy()
  #     self._feedbacks.clear()
  #     for (type, x, y) in feedbacks:
  #       self._feedback_handler.handleFeedback(type, x, y)
  #   # else:
  #   #   for (type, x, y) in self.feedbacks:
  #   #     print("unhandled FB: " + self.layer_id + '.' + type + ':' + str(x) + ',' + str(y))



