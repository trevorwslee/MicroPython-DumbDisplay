from dumbdisplay import *
from dumbdisplay_examples.tamagotchi.common import Panel, Image


class FoodPanel(Panel):
    def __init__(self, x, y, width, height):
        self.box_image_name = "buttonSquare_beige_pressed.png"
        self.food_image_names = ["food_1.png", "food_2.png", "food_3.png"]
        self.box_1 = Image(x - 250, y, 150, 150, self.box_image_name)
        super().__init__(x, y, width, height, image_name="panel_brown.png", text=None)

    def initialize(self, layer: LayerGraphical, *, set_init_visibility: bool = None):
        self.box_1.initialize(layer, set_init_visibility=set_init_visibility)
        super().initialize(layer, set_init_visibility=set_init_visibility)

    def set_visible(self, visible: bool):
        super().set_visible(visible=visible)
        self.box_1.set_visible(visible=visible)