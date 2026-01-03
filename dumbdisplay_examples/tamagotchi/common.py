from enum import Enum
from typing import Callable, Any

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

    def check_clicked(self, x, y) -> bool:
        return (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)


class BaseUIComponent(UIComponent):
    def __init__(self, component_type: str, x: int, y: int, width: int, height: int, *, xy_is_center: bool = False):
        super().__init__(x, y, width, height, xy_is_center=xy_is_center)
        global _next_level_id
        self._visible = False
        self._level_id = f"{component_type}-{_next_level_id}"
        _next_level_id += 1

    def initialize(self, layer: LayerGraphical, *, init_visible: bool):
        self.layer = layer
        self._visible = init_visible
        layer.addLevel(self._level_id, width=self.width, height=self.height, switch_to_it=True)
        layer.levelTransparent(not self._visible)
        layer.setLevelAnchor(self.x, self.y)

    def is_visible(self) -> bool:
        return self._visible

    def set_visible(self, visible: bool):
        self._visible = visible
        self.layer.pushLevelAndSwitchTo(self._level_id)
        self.layer.levelTransparent(not visible)
        self.layer.popLevel()

    def act_on(self, action: Callable[[LayerGraphical], Any]) -> Any:
        self.layer.pushLevelAndSwitchTo(self._level_id)
        res = action(self.layer)
        self.layer.popLevel()
        return res



class StdUIComponentBase(BaseUIComponent):
    def __init__(self, component_type: str, x: int, y: int, width: int, height: int, *,
                 background_image_name: str = None, image_name: str = None, text: str = None,
                 xy_is_center: bool = False):
        super().__init__(component_type, x, y, width, height, xy_is_center=xy_is_center)
        self.background_image_name = background_image_name
        self.image_name = image_name
        self.text_lines = text.splitlines() if text is not None else None

    def initialize(self, layer: LayerGraphical, *, init_visible: bool = True):
        super().initialize(layer, init_visible=init_visible)
        if self.background_image_name is not None:
            layer.setLevelBackground("", self.background_image_name)
        if self.image_name is not None:
            layer.drawImageFile(self.image_name, 0, 0, self.width, self.height)
        if self.text_lines is not None:
            text_size = 32
            if len(self.text_lines) == 1:
                text_len = len(self.text_lines[0])
                if text_len >= 5:
                    text_size -= (text_len - 3)
                    if text_size < 8:
                        text_size = 8
            layer.setTextSize(text_size)
            layer.setTextFont("DL::Roboto")
            layer.setTextColor("white")
            line_height = 40
            y = (self.height - line_height * len(self.text_lines)) // 2
            for text in self.text_lines:
                layer.drawTextLine(text, y, align='C')
                y += line_height

    def animate_background_image(self, fps: float = 0, reset: bool = True, options: str = ""):
        self.layer.animateLevelBackground(fps=fps, reset=reset, options=options)

    def stop_animate_background_image(self, reset: bool = True):
        self.layer.stopAnimateLevelBackground(reset=reset)


class StandardUIComponent(StdUIComponentBase):
    def __init__(self, x: int, y:int , width: int, height: int, *,
                 background_image_name: str = None, image_name: str = None, text: str = None,
                 xy_is_center: bool = False):
        super().__init__("std", x, y, width, height, background_image_name=background_image_name, image_name=image_name, text=text, xy_is_center=xy_is_center)


class Image(StdUIComponentBase):
    def __init__(self, x: int, y:int , width: int, height: int, image_name: str, *, xy_is_center: bool = False):
        super().__init__("img", x, y, width, height, image_name=image_name, xy_is_center=xy_is_center)


class Button(StdUIComponentBase):
    def __init__(self, x: int, y:int , width: int, height: int, image_name: str, text: str = None, *, xy_is_center: bool = True):
        super().__init__("btn", x, y, width, height, image_name=image_name, text=text, xy_is_center=xy_is_center)

class Panel(StdUIComponentBase):
    def __init__(self, x: int, y: int, width: int, height: int, image_name: str, text: str):
        super().__init__("panel", x, y, width, height, image_name=image_name, text=text, xy_is_center=True)
        self.exit_btn = Button(self.x + 35, self.y + 25, icon_cross_width, icon_cross_height, icon_cross_image_name, xy_is_center=False)
        #self.exit_btn = Button(75, 65, icon_cross_width, icon_cross_height, icon_cross_image_name, init_visible=False)

    def initialize(self, layer: LayerGraphical, *, init_visible: bool):
        self.exit_btn.initialize(layer, init_visible=init_visible)
        super().initialize(layer, init_visible=init_visible)

    def set_visible(self, visible: bool):
        self.exit_btn.set_visible(visible=visible)
        super().set_visible(visible=visible)

    def get_image_names(self) -> list[str]:
        image_names = [self.image_name, self.exit_btn.image_name]
        return image_names

    def check_clicked_cross(self, x, y) -> bool:
        return self.exit_btn.check_clicked(x, y)


class StageBase:
    def __init__(self, app: DDAppBase, stage_layer: LayerGraphical, init_visible: bool = True):
        self.app = app
        self.stage_layer = stage_layer
        self._visible = init_visible
        stage_layer.visibility(init_visible)

    def update(self):
        pass

    def handle_clicked(self, pos_x: int, pos_y: int):
        raise Exception("subclass must implement handleClicked method")

    def is_visible(self) -> bool:
        return self._visible

    def set_visible(self, visible: bool):
        self._visible = visible
        self.stage_layer.visibility(visible)
