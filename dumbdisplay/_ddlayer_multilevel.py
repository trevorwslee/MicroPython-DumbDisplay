from dumbdisplay._ddlayer import DDLayer, _DD_BOOL_ARG, _DD_FLOAT_ARG

DD_DEF_LAYER_LEVEL_ID = "_"

class DDLayerMultiLevel(DDLayer):
    def __init__(self, dd, layer_id):
        super().__init__(dd, layer_id)
    def addLevel(self, level_id: str, width: float, height: float, switchToIt: bool = False):
        '''
        add a level, optionally change its "opening" size
        :param level_id: level ID; cannot be DD_DEF_LAYER_LEVEL_ID
        :param width: width width of the level "opening"; 0 means the maximum width (the width of the layer)
        :param height: height height of the level "opening"; 0 means the maximum height (the height of the layer)
        :param switchToIt:
        :return:
        '''
        self.dd._sendCommand(self.layer_id, "addlevel", level_id, _DD_FLOAT_ARG(width), _DD_FLOAT_ARG(height), _DD_BOOL_ARG(switchToIt))
    # TODO: add more
