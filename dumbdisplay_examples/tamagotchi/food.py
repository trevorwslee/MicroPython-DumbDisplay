from dumbdisplay import *
from dumbdisplay_examples.tamagotchi.action import action
from dumbdisplay_examples.tamagotchi.common import Panel, Image, StdUIComponentBase
from dumbdisplay_examples.tamagotchi.sound import play_coin_sound


class FoodBox(StdUIComponentBase):
    def __init__(self, x: int, y:int , width: int, height: int, food_image_name: str, food_width: int, food_height: int, *, xy_is_center = True):
        self.food_image = Image(x, y, food_width, food_height, food_image_name, xy_is_center=xy_is_center)
        super().__init__("foodbox", x, y, width, height, image_name="buttonSquare_beige_pressed.png", xy_is_center=xy_is_center)

    def initialize(self, layer: LayerGraphical, *, init_visible: bool):
        self.food_image.initialize(layer, init_visible=init_visible)
        super().initialize(layer, init_visible=init_visible)

    def set_visible(self, visible: bool):
        self.food_image.set_visible(visible=visible)
        super().set_visible(visible=visible)

    def get_image_names(self) -> list[str]:
        image_names = [self.image_name, self.food_image.image_name]
        return image_names


class FoodPanel(Panel):
    def __init__(self, x, y, width, height):
        self.food_boxes = [
            FoodBox(x - 220, y + 20, 150, 150, "food_1.png", 100, 100),
            FoodBox(x, y + 20, 150, 150, "food_2.png", 75, 100),
            FoodBox(x + 220, y + 20, 150, 150, "food_3.png", 100, 100)
        ]
        super().__init__(x, y, width, height, image_name="panel_brown.png", text=None)

    def initialize(self, layer: LayerGraphical, *, init_visible: bool):
        for food_box in self.food_boxes:
            food_box.initialize(layer, init_visible=init_visible)
        super().initialize(layer, init_visible=init_visible)

    def set_visible(self, visible: bool):
        for food_box in self.food_boxes:
            food_box.set_visible(visible=visible)
        super().set_visible(visible=visible)

    def get_image_names(self) -> list[str]:
        image_names = super().get_image_names()
        for food_box in self.food_boxes:
            image_names += food_box.get_image_names()
        return image_names

    def handle_clicked(self, pos_x: int, pos_y: int) -> bool:
        for (idx, foodbox) in enumerate(self.food_boxes):
            if foodbox.check_clicked(pos_x, pos_y):
                if idx == 0:
                    if action['satiety'] + 3 <= 100 and action['logiki'] - 5 >= 0:
                        play_coin_sound()
                        action['satiety'] += 3
                        action['toilet'] -= 3
                        action['logiki'] -= 5
                        return True
                    else:
                        print(f"xxx cannot eat food 0: satiety+3={action['satiety']+3}, logiki-5={action['logiki']-5}")
                        return False
                elif idx == 1:
                    if action['satiety'] + 6 <= 100 and action['logiki'] - 10 >= 0:
                        play_coin_sound()
                        action['satiety'] += 6
                        action['toilet'] -= 6
                        action['logiki'] -= 10
                        return True
                    else:
                        print(f"xxx cannot eat food 1: satiety+6={action['satiety']+6}, logiki-10={action['logiki']-10}")
                        return False
                elif idx == 2:
                    if action['satiety'] + 10 <= 100 and action['logiki'] - 15 >= 0:
                        play_coin_sound()
                        action['satiety'] += 10
                        action['toilet'] -= 10
                        action['logiki'] -= 15
                        return True
                    else:
                        print(f"xxx cannot eat food 2: satiety+10={action['satiety']+10}, logiki-15={action['logiki']-15}")
                        return False
        return False


