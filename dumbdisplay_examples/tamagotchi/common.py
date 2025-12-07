from enum import Enum
from dumbdisplay import *

_next_level_id = 1

icon_cross_image_name = "iconCross_beige.png"
icon_cross_width = 40
icon_cross_height = 40


class UIComponent:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def checkClicked(self, x, y) -> bool:
        return (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)



class ImageUIComponent(UIComponent):
    def __init__(self, component_type: str, x: int, y: int, width: int, height: int, image_name: str, text: str = None):
        super().__init__(x, y, width, height)
        global _next_level_id
        self.image_name = image_name
        self.text_lines = text.splitlines() if text is not None else []
        self._visible = False
        self._level_id = f"{component_type}-{_next_level_id}"
        _next_level_id += 1

    def initialize(self, stage_layer: LayerGraphical, init_visible: bool = True):
        self.stage_layer = stage_layer
        self._visible = init_visible
        stage_layer.addLevel(self._level_id, width=self.width, height=self.height, switch_to_it=True)
        if not init_visible:
            stage_layer.levelTransparent(True)
        stage_layer.setLevelAnchor(self.x, self.y)
        #stage_layer.drawImageFileFit(self.image_name, 0, 0, self.width, self.height)
        stage_layer.drawImageFile(self.image_name, 0, 0, self.width, self.height)
        if self.text_lines is not None:
            stage_layer.setTextSize(32)
            stage_layer.setTextFont("DL::Roboto")
            stage_layer.setTextColor("white")
            line_height = 40
            y = (self.height - line_height * len(self.text_lines)) // 2
            for text in self.text_lines:
                stage_layer.drawTextLine(text, y, align='C')
                y += line_height

    def is_visible(self) -> bool:
        return self._visible

    def set_visible(self, visible: bool):
        self._visible = visible
        self.stage_layer.pushLevelAndSwitchTo(self._level_id)
        self.stage_layer.levelTransparent(not visible)
        self.stage_layer.popLevel()


class Button(ImageUIComponent):
    def __init__(self, x: int, y:int , width: int, height: int, image_name: str, text: str = None):
        super().__init__("btn", x, y, width, height, image_name, text)

    def initialize(self, stage_layer: LayerGraphical, init_visible: bool = True):
        super().initialize(stage_layer, init_visible)


class Panel(ImageUIComponent):
    def __init__(self, x: int, y: int, width: int, height: int, image_name: str, text: str):
        super().__init__("panel", x, y, width, height, image_name, text)
        self.exit_btn = Button(x + 35, y + 25, icon_cross_width, icon_cross_height, icon_cross_image_name)

    def initialize(self, stage_layer: LayerGraphical, init_visible: bool = True):
        self.exit_btn.initialize(stage_layer, init_visible)
        super().initialize(stage_layer, init_visible)

    def set_visible(self, visible: bool):
        self.exit_btn.set_visible(visible=visible)
        super().set_visible(visible=visible)

    def checkClickedCross(self, x, y) -> bool:
        return self.exit_btn.checkClicked(x, y)


class Scene(Enum):
    MENU = 1


class StageBase:
    def __init__(self, app: 'TamagotchiApp', stage_layer: LayerGraphical):
        self.app = app
        self.stage_layer = stage_layer
    def handleClicked(self, pos_x: int,  pos_y: int):
        raise NotImplementedError()
