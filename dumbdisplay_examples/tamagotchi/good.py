from dumbdisplay_examples.tamagotchi.common import Panel


class FoodPanel(Panel):
    def __init__(self, x, y, width, height, image_name):
        super().__init__(x, y, width, height, image_name, text=None)