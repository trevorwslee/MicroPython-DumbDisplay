from dumbdisplay import *
from dumbdisplay_examples.tamagotchi.common import Panel, Image, StdUIComponentBase


class FoodBox(StdUIComponentBase):
    def __init__(self, x: int, y:int , width: int, height: int, food_image_name: str, *, init_visible: bool = False, xy_is_center = True):
        super().__init__("foodbox", x, y, width, height, image_name="buttonSquare_beige_pressed.png", init_visible=init_visible, xy_is_center=xy_is_center)
        self.food_image_name = food_image_name

    def initialize(self, layer: LayerGraphical, *, set_init_visibility: bool = None):
        super().initialize(layer, set_init_visibility=set_init_visibility)

    def set_visible(self, visible: bool):
        super().set_visible(visible=visible)

    def get_image_names(self) -> list[str]:
        image_names = [self.image_name, self.food_image_name]
        return image_names


class FoodPanel(Panel):
    def __init__(self, x, y, width, height):
        self.food_boxes = [
            FoodBox(x - 250, y, 150, 150, "food_1.png"),
            FoodBox(x, y, 150, 150, "food_2.png"),
            FoodBox(x + 250, y, 150, 150, "food_3.png")
        ]
        super().__init__(x, y, width, height, image_name="panel_brown.png", text=None)

    def initialize(self, layer: LayerGraphical, *, set_init_visibility: bool = None):
        for food_box in self.food_boxes:
            food_box.initialize(layer, set_init_visibility=set_init_visibility)
        super().initialize(layer, set_init_visibility=set_init_visibility)

    def set_visible(self, visible: bool):
        for food_box in self.food_boxes:
            food_box.set_visible(visible=visible)
        super().set_visible(visible=visible)

    def get_image_names(self) -> list[str]:
        image_names = super().get_image_names()
        for food_box in self.food_boxes:
            image_names += food_box.get_image_names()
        return image_names
