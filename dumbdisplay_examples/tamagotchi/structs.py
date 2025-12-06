from enum import Enum
from dumbdisplay import *

_next_level_id = 1

class Button:
    def __init__(self, x: int, y:int , width: int, height: int, image_name: str, text: str = None):
        global _next_level_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_name = image_name
        self.text = text
        self.level_id = f"btn-{_next_level_id}"
        _next_level_id += _next_level_id

    def _init_game_object_layer(self, stage_layer: LayerGraphical, init_visible: bool = True):
        self.stage_layer = stage_layer
        stage_layer.addLevel(self.level_id, width=self.width, height=self.height, switch_to_it=True)
        if not init_visible:
            stage_layer.levelTransparent(True)
        stage_layer.setLevelAnchor(self.x, self.y)
        stage_layer.drawImageFileFit(self.image_name, 0, 0, self.width, self.height)
        #stage_layer.drawImageFileFit(self.image_name)
        if self.text is not None:
            stage_layer.setTextSize(32)
            stage_layer.setTextFont("DL::Roboto")
            stage_layer.setTextColor("white")
            stage_layer.drawTextLine(self.text, 0, align='C')

    def set_visible(self, visible: bool):
        self.stage_layer.selectLevel(self.level_id)
        self.stage_layer.levelTransparent(not visible)

    def collidepoint(self, x, y):
        return (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)


class Panel:
    def __init__(self, x: int, y: int, width: int, height: int, image_name: int, text: str = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_lines = text.splitlines() if text is not None else []



class Scene(Enum):
    MENU = 1


class StageBase:
    def __init__(self, app: 'TamagotchiApp', stage_layer: LayerGraphical):
        self.app = app
        self.stage_layer = stage_layer
    def handleClicked(self, pos_x: int,  pos_y: int):
        raise NotImplementedError()
