from ._ddlayer import DDLayer
from ._ddlayer import _DD_BOOL_ARG
from ._ddlayer import _DD_COLOR_ARG

class DDLayerPlotter(DDLayer):
  '''Plotter'''
  def __init__(self, dd, width, height, pixels_per_second = 10):
    '''
    :param dd: DumbDisplay object
    :param width: width
    :param height: height
    :param pixels_per_second: # pixel to scroll per second
    '''
    layer_id = dd._createLayer(str("plotterview"), str(width), str(height), str(pixels_per_second))
    super().__init__(dd, layer_id)
  def label(self, **key_label_pairs):
    '''set labels of keys; if key has no label, the key will be the label'''
    for (key, lab) in key_label_pairs.items():
      self.dd._sendCommand(self.layer_id, "label", key, str(lab))
  def set(self, **key_value_pairs):
    '''set values with multiple key value pairs; value should be numeric'''
    params = []
    for (k, v) in key_value_pairs.items():
      params.append(k)
      params.append(str(v))
    self.dd._sendCommand(self.layer_id, "", *params)
