from dumbdisplay.ddcmds import DDC_setlevelanchor, DDC_movelevelanchorby, DDC_setlevelrotate
from dumbdisplay.ddimpl import DumbDisplayImpl
from dumbdisplay.ddlayer import DDLayer, _DD_BOOL_ARG, _DD_FLOAT_ARG, _DD_INT_ARG, _DD_FLOAT_IS_ZERO

DD_DEF_LAYER_LEVEL_ID = "_"

class DDLayerMultiLevel(DDLayer):
    def __init__(self, dd: DumbDisplayImpl, layer_id: str):
        super().__init__(dd, layer_id)
    def addLevel(self, level_id: str, width: float = 0, height: float = 0, switch_to_it: bool = False):
        """
        add a level, optionally change its "opening" size
        :param level_id: level ID; cannot be DD_DEF_LAYER_LEVEL_ID
        :param width: width of the level "opening"; 0 means the maximum width (the width of the layer)
        :param height: height of the level "opening"; 0 means the maximum height (the height of the layer)
        """
        if _DD_FLOAT_IS_ZERO(width) and _DD_FLOAT_IS_ZERO(height):
            if switch_to_it:
                self.dd._sendCommand(self.layer_id, "addlevel", level_id, _DD_BOOL_ARG(switch_to_it))
            else:
                self.dd._sendCommand(self.layer_id, "addlevel", level_id)
        else:
            self.dd._sendCommand(self.layer_id, "addlevel", level_id, _DD_FLOAT_ARG(width), _DD_FLOAT_ARG(height), _DD_BOOL_ARG(switch_to_it))
    def addTopLevel(self, level_id: str, width: float = 0, height:float = 0, switch_to_it:bool = False):
        """
        add top level -- like addLevel() but add to the top (i.e. will be drawn last)
        :param level_id: level ID; cannot be DD_DEF_LAYER_LEVEL_ID
        :param width: width of the level "opening"; 0 means the maximum width (the width of the layer)
        :param height: height of the level "opening"; 0 means the maximum height (the height of the layer)
        """
        if _DD_FLOAT_IS_ZERO(width) and _DD_FLOAT_IS_ZERO(height):
            if switch_to_it:
                self.dd._sendCommand(self.layer_id, "addtoplevel", level_id, _DD_BOOL_ARG(switch_to_it))
            else:
                self.dd._sendCommand(self.layer_id, "addtoplevel", level_id)
        else:
            self.dd._sendCommand(self.layer_id, "aaddtoplevel", level_id, _DD_FLOAT_ARG(width), _DD_FLOAT_ARG(height), _DD_BOOL_ARG(switch_to_it))
    def switchLevel(self, level_id: str, add_if_missing: bool  = True):
        """
        switch to a different level (which is like a sub-layer), making it the current level
        :param add_if_missing: if true, add the level if it is missing 
        """
        self.dd._sendCommand(self.layer_id, "switchlevel", level_id, _DD_BOOL_ARG(add_if_missing))
    def pushLevel(self):
        """
        push the current level onto the level stack, to be pop with popLevel()
        """
        self.dd._sendCommand(self.layer_id, "pushlevel")
    def pushLevelAndSwitchTo(self, switch_tolevel_id: str, add_if_missing: bool = True):
        """
        push the current level onto the level stack, to be pop with popLevel()
        :param switch_tolevel_id switch to level ID (after pushing current level)
        """
        self.dd._sendCommand2(self.layer_id, "pushlevel", switch_tolevel_id, _DD_BOOL_ARG(add_if_missing))
    def popLevel(self):
        """
        pop a level from the level stack and make it the current level
        """
        self.dd._sendCommand2(self.layer_id, "poplevel")
    def levelOpacity(self, opacity: int):
        """
        set the opacity of the current level
        :param opacity background opacity (0 - 100)
        """
        self.dd._sendCommand(self.layer_id, "levelopacity", _DD_INT_ARG(opacity))
    def levelTransparent(self, transparent: bool):
        """
        set whether level is transparent
        """
        self.dd._sendCommand(self.layer_id, "leveltransparent", _DD_INT_ARG(transparent))
    def setLevelAnchor(self, x: float, y: float, reach_in_millis: int = 0):
        """
        set the anchor of the level; note that level anchor is the top-left corner of the level "opening"
        """
        #command = "setlevelanchor" if self.dd._compatibility < 15 else "SLA"
        if reach_in_millis > 0:
            self.dd._sendCommand(self.layer_id, DDC_setlevelanchor, _DD_FLOAT_ARG(x), _DD_FLOAT_ARG(y), _DD_INT_ARG(reach_in_millis))
        else:
            self.dd._sendCommand(self.layer_id, DDC_setlevelanchor, _DD_FLOAT_ARG(x), _DD_FLOAT_ARG(y))
    def moveLevelAnchorBy(self, by_x: float, by_y: float, reach_in_millis: int = 0):
        """
        move the level anchor
        """
        #command = "movelevelanchorby" if self.dd._compatibility < 15 else "MLAB"
        if reach_in_millis > 0:
            self.dd._sendCommand(self.layer_id, DDC_movelevelanchorby, _DD_FLOAT_ARG(by_x), _DD_FLOAT_ARG(by_y), _DD_INT_ARG(reach_in_millis));
        else:
            self.dd._sendCommand(self.layer_id, DDC_movelevelanchorby, _DD_FLOAT_ARG(by_x), _DD_FLOAT_ARG(by_y))
    def setLevelRotation(self, angle: float, pivot_x: float = 0, pivot_y: float = 0, reach_in_millis: int = 0):
        """
        :param angle: rotation angle in degree; positive is clockwise
        :param pivot_x: x coordinate of the pivot point (relative to the level anchor)
        :param pivot_y: y coordinate of the pivot point (relative to the level anchor)
        """
        if reach_in_millis > 0:
            self.dd._sendCommand(self.layer_id, DDC_setlevelrotate, _DD_FLOAT_ARG(angle), _DD_FLOAT_ARG(pivot_x), _DD_FLOAT_ARG(pivot_y), _DD_INT_ARG(reach_in_millis))
        else:
            angle_is_zero = _DD_FLOAT_IS_ZERO(angle)
            pivot_x_is_zero = _DD_FLOAT_IS_ZERO(pivot_x)
            pivot_y_is_zero = _DD_FLOAT_IS_ZERO(pivot_y)
            if angle_is_zero:
                self.dd._sendCommand(self.layer_id, DDC_setlevelrotate)
            elif pivot_x_is_zero and pivot_y_is_zero:
                self.dd._sendCommand(self.layer_id, DDC_setlevelrotate, _DD_FLOAT_ARG(angle))
            elif pivot_y_is_zero:
                self.dd._sendCommand(self.layer_id, DDC_setlevelrotate, _DD_FLOAT_ARG(angle), _DD_FLOAT_ARG(pivot_x))
            else:
                self.dd._sendCommand(self.layer_id, DDC_setlevelrotate, _DD_FLOAT_ARG(angle), _DD_FLOAT_ARG(pivot_x), _DD_FLOAT_ARG(pivot_y))
    def registerLevelBackground(self, background_id: str, background_image_name: str, draw_background_options: str = ""):
        """
        register an image for setting as level's background
        :param background_id id to identify the background -- see setLevelBackground()
        :param background_image_name name of the image
                                   can be a series of images like dumbdisplay_##0-7##.png (for dumbdisplay_0.png to dumbdisplay_7.png)
                                   which can be used for animation with animateLevelBackground()
        :param drawBackgroundOptions options for drawing the background; same means as the option param of GraphicalDDLayer::drawImageFiler()
        """
        self.dd._sendCommand(self.layer_id, "reglevelbg", background_id, background_image_name, draw_background_options)
    def exportLevelAsRegisteredBackground(self, background_id: str, replace: bool = True):
        """
        experimental:
        export the current level as a registered background image -- see exportLevelsAsImage() and registerLevelBackground()
        :param background_id id to identify the background -- see setLevelBackground()
        :param replace if true (default), replace the existing registered background image with the same id;
                      if false, will add as an item of background image series that can be used for animation with animateLevelBackground()
        """
        self.dd.sendCommand(self.layer_id, "explevelasregbg", background_id, _DD_BOOL_ARG(replace))
    def setLevelBackground(self, background_id: str, background_image_name: str = "", draw_background_options: str = ""):
        """
        set a registered background image as the current level's background
        :param background_id can be the empty str ""
        :param background_image_name if not registered, the name of the image to register;
                                     can be a series of images like dumbdisplay_##0-7##.png (for dumbdisplay_0.png to dumbdisplay_7.png)
                                     which can be used for animation with animateLevelBackground()
        :param draw_background_options if not registered, the options for drawing the background
        """
        if background_image_name == "":
            self.dd._sendCommand(self.layer_id, "setlevelbg", background_id)
        else:
            self.dd._sendCommand(self.layer_id, "setlevelbg", background_id, background_image_name, draw_background_options)
    def setLevelNoBackground(self):
        """
        set that the current level uses no background image
        """
        self.dd._sendCommand(self.layer_id, "setlevelnobg")
    def animateLevelBackground(self, fps: float = 0, reset: bool = True, options: str = ""):
        """
        start animate level background (if level background has a series of images)
        :param fps frames per second which is used to calculate the interval between the series of images
        :param reset to the first image in the series (before start animation)
        param options can be "r" to reverse the order of the series of images
        """
        if not reset or options != "":
            self.dd._sendCommand(self.layer_id, "anilevelbg", _DD_FLOAT_ARG(fps), _DD_BOOL_ARG(reset), options)
        else:
            if _DD_FLOAT_IS_ZERO(fps):
                self.dd._sendCommand(self.layer_id, "anilevelbg")
            else:
                self.dd._sendCommand(self.layer_id, "anilevelbg", _DD_FLOAT_ARG(fps))
    def stopAnimateLevelBackground(self, reset: bool = True):
        """
        stop animate level background
        :param reset reset to the first image in the series
        """
        self.dd._sendCommand(self.layer_id, "stopanilevelbg", _DD_FLOAT_ARG(reset))
    def reorderLevel(self, level_id: str, how: str):
        """
        reorder the specified level (by moving it in the z-order plane)
        :param how  can be "T" for top; or "B" for bottom; "U" for up; or "D" for down
        """
        self.dd._sendCommand(self.layer_id, "reordlevel", level_id, how)
    def exportLevelsAsImage(self, image_file_name: str, cache_it_not_save: bool = False):
        """
        export (and save) the levels as an image (without the decorations of the layer like border)
        """
        self.dd._sendCommand(self.layer_id, "explevelsasimg", image_file_name, _DD_BOOL_ARG(cache_it_not_save))
    def deleteLevel(self, level_id: str):
        """
        delete the specified level
        """
        self.dd._sendCommand(self.layer_id, "dellevel", level_id)

