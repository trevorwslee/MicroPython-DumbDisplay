

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


class DDLayer:
  def __init__(self, dd, layer_id):
    self.dd = dd
    self.layer_id = layer_id
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
  def enableFeedback(self, auto_feedback_method = ""):
    '''
    rely on getFeedback() being called */
    :param auto_feedback_method:
    . "" -- no auto feedback
    . "f" -- flash the default way (layer + border)
    . "fl" -- flash the layer
    . "fa" -- flash the area where the layer is clicked
    . "fas" -- flash the area (as a spot) where the layer is clicked
    '''
    self.dd._sendCommand(self.layer_id, "feedback", _DD_BOOL_ARG(True), auto_feedback_method)
  # feedbackHandler = NULL;
  # if (pFeedbackManager != NULL)
  #   delete pFeedbackManager;
  # pFeedbackManager = new DDFeedbackManager(FEEDBACK_BUFFER_SIZE + 1);  // need 1 more slot
  def disableFeedback(self):
    """disable feedback"""
    self.dd._sendCommand(self.layer_id, "feedback", _DD_BOOL_ARG(False))
  # feedbackHandler = NULL;
  # if (pFeedbackManager != NULL) {
  # delete pFeedbackManager;
  # pFeedbackManager = NULL;
  # }
  def release(self):
    self.dd._deleteLayer(self.layer_id)


