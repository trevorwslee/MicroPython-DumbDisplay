from enum import Enum
from dumbdisplay import *
from dumbdisplay_examples.utils import DDAppBase

_next_level_id = 1

icon_cross_image_name = "iconCross_beige.png"
icon_cross_width = 40
icon_cross_height = 40


class UIComponent:
    def __init__(self, x: int, y: int, width: int, height: int, xy_is_center: bool = True):
        if xy_is_center:
            x = x - width // 2
            y = y - height // 2
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def checkClicked(self, x, y) -> bool:
        return (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)


class LevelUIComponent(UIComponent):
    def __init__(self, component_type: str, x: int, y: int, width: int, height: int, *, init_visible: bool = True, xy_is_center: bool = False):
        super().__init__(x, y, width, height, xy_is_center=xy_is_center)
        global _next_level_id
        self._visible = init_visible
        self._level_id = f"{component_type}-{_next_level_id}"
        _next_level_id += 1

    def initialize(self, stage_layer: LayerGraphical, *, set_init_visibility: bool = None):
        self.stage_layer = stage_layer
        if set_init_visibility is not None:
            self._visible = set_init_visibility
        stage_layer.addLevel(self._level_id, width=self.width, height=self.height, switch_to_it=True)
        stage_layer.levelTransparent(not self._visible)
        stage_layer.setLevelAnchor(self.x, self.y)

    def is_visible(self) -> bool:
        return self._visible

    def set_visible(self, visible: bool):
        self._visible = visible
        self.stage_layer.pushLevelAndSwitchTo(self._level_id)
        self.stage_layer.levelTransparent(not visible)
        self.stage_layer.popLevel()


class ImageUIComponent(LevelUIComponent):
    def __init__(self, component_type: str, x: int, y: int, width: int, height: int, image_name: str, text: str = None, *, init_visible: bool = True, xy_is_center: bool = False):
        super().__init__(component_type, x, y, width, height, init_visible=init_visible, xy_is_center=xy_is_center)
        self.image_name = image_name
        self.text_lines = text.splitlines() if text is not None else None

    def initialize(self, stage_layer: LayerGraphical, *, set_init_visibility: bool = None):
        super().initialize(stage_layer, set_init_visibility=set_init_visibility)
        stage_layer.drawImageFile(self.image_name, 0, 0, self.width, self.height)
        if self.text_lines is not None:
            text_size = 32
            if len(self.text_lines) == 1:
                text_len = len(self.text_lines[0])
                if text_len >= 5:
                    text_size -= (text_len - 3)
                    if text_size < 8:
                        text_size = 8
            stage_layer.setTextSize(text_size)
            stage_layer.setTextFont("DL::Roboto")
            stage_layer.setTextColor("white")
            line_height = 40
            y = (self.height - line_height * len(self.text_lines)) // 2
            for text in self.text_lines:
                stage_layer.drawTextLine(text, y, align='C')
                y += line_height


class Image(ImageUIComponent):
    def __init__(self, x: int, y:int , width: int, height: int, image_name: str, *, init_visible: bool = True):
        super().__init__("img", x, y, width, height, image_name, init_visible=init_visible)

    def initialize(self, stage_layer: LayerGraphical, *, set_init_visibility: bool = None):
        super().initialize(stage_layer, set_init_visibility=set_init_visibility)


class Button(ImageUIComponent):
    def __init__(self, x: int, y:int , width: int, height: int, image_name: str, text: str = None, *, init_visible: bool = True):
        super().__init__("btn", x, y, width, height, image_name, text, init_visible=init_visible, xy_is_center=True)

    def initialize(self, stage_layer: LayerGraphical, *, set_init_visibility: bool = None):
        super().initialize(stage_layer, set_init_visibility=set_init_visibility)


class Panel(ImageUIComponent):
    def __init__(self, x: int, y: int, width: int, height: int, image_name: str, text: str):
        super().__init__("panel", x, y, width, height, image_name, text, init_visible=False)
        self.exit_btn = Button(x + 50, y + 40, icon_cross_width, icon_cross_height, icon_cross_image_name, init_visible=False)

    def initialize(self, stage_layer: LayerGraphical, *, set_init_visibility: bool = None):
        self.exit_btn.initialize(stage_layer, set_init_visibility=set_init_visibility)
        super().initialize(stage_layer, set_init_visibility=set_init_visibility)

    def set_visible(self, visible: bool):
        self.exit_btn.set_visible(visible=visible)
        super().set_visible(visible=visible)

    def checkClickedCross(self, x, y) -> bool:
        return self.exit_btn.checkClicked(x, y)


class Scene(Enum):
    MENU = 1,
    GAME = 2,


class StageBase:
    def __init__(self, app: DDAppBase, stage_layer: LayerGraphical, init_visible: bool = True):
        self.app = app
        self.stage_layer = stage_layer
        self._visible = init_visible
        stage_layer.visibility(init_visible)

    def handleClicked(self, pos_x: int,  pos_y: int):
        raise Exception("subclass must implement handleClicked method")

    def is_visible(self) -> bool:
        return self._visible

    def set_visible(self, visible: bool):
        self._visible = visible
        self.stage_layer.visibility(visible)
