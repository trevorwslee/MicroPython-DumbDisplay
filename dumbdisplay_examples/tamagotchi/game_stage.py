import random
import time

from dumbdisplay import *
from dumbdisplay_examples.tamagotchi.common import Button, Panel, StageBase, BaseUIComponent, Image, \
    StdUIComponentBase, StandardUIComponent
from dumbdisplay_examples.tamagotchi.good import FoodPanel
from dumbdisplay_examples.utils import DDAppBase



_timeout = 15

_background_image_name = "background.jpg"

_tamagotchi_image_name_prefix = "tamagotchi-"
_tamagotchi_image_name_count = 8
_tamagotchi_image_name = "tamagotchi-##0-7##.png"  # encoded for animation



_info_satiety = Button(20, 30, 25, 50, "lightning.png")
_info_toilet = Button(150, 30, 50, 50, "toilet.png")
_info_happy = Button(270, 30, 50, 50, "smile.png")
_info_health = Button(30, 90, 60, 60, "health.png")

_day_image = Image(735, 70, 50, 50, "day.png")
_night_image = Image(735, 70, 50, 50, "night.png", init_visible=False)
_sleep_image = Image(430, 350, 50, 50, "sleep.png", init_visible=False)

tamagotchi = StandardUIComponent(330, 340, 150, 150, background_image_name=_tamagotchi_image_name)


btn_statistic = Button(715, 40, 150, 50, "buttonLong_brown.png", "Statistic")

btn_satiety = Button(85, 467, 150, 50, "buttonLong_brown.png", "Feed")
btn_toilet = Button(285, 467, 150, 50, "buttonLong_brown.png", "Clear")
btn_play = Button(515, 467, 150, 50, "buttonLong_brown.png", "Play")
btn_health = Button(715, 467, 150, 50, "buttonLong_brown.png", "Medicine")


_food = FoodPanel(25, 50, 750, 400, "panel_brown.png")


_init_action = {'satiety': 100, 'toilet': 100, 'happy': 100, 'health': 100, 'logiki': 50}

_action = _init_action.copy()

class ActionText(BaseUIComponent):
    def __init__(self, x, y, action_key: str):
        super().__init__("acttxt", x, y, 50, 30)
        self.x = x
        self.y = y
        self.action_key = action_key
        self._drawn_text = None

    def initialize(self, layer: LayerGraphical, *, set_init_visibility: bool = None):
        super().initialize(layer, set_init_visibility=set_init_visibility)
        text_size = 24
        layer.setTextSize(text_size)
        layer.setTextFont("DL::Roboto")
        layer.setTextColor("green")
        self.update_text()

    def update_text(self):
        text = _action[self.action_key].__str__()
        if text != self._drawn_text:
            self.layer.pushLevelAndSwitchTo(self._level_id)
            self.layer.clear()
            self.layer.drawTextLine(text)
            self.layer.popLevel()
            self._drawn_text = text


_satiety_text = ActionText(40, 15, "satiety")
_toilet_text = ActionText(180, 15, "toilet")
_smile_text = ActionText(300, 15, "happy")
_health_text = ActionText(70, 75, "health")


_game_buttons = [_info_satiety, _info_toilet, _info_happy, _info_health,
                 btn_statistic,
                 btn_satiety, btn_toilet, btn_play, btn_health]
_game_images = [_day_image, _night_image, _sleep_image]
_game_texts = [_satiety_text, _toilet_text, _smile_text, _health_text]



# def reset_game_stage():
#     global _action
#     _action = _init_action.copy()

def get_game_stage_image_names():
    image_names = [_background_image_name]
    image_names.append(_food.image_name)
    for i in range(_tamagotchi_image_name_count):
        image_name = f"{_tamagotchi_image_name_prefix}{i}.png"
        image_names.append(image_name)
    for menu_button in _game_buttons:
        image_names.append(menu_button.image_name)
    for game_image in _game_images:
        image_names.append(game_image.image_name)
    return image_names


def setup_game_stage_layer(app: DDAppBase, game_stage_layer: LayerGraphical) -> 'GameStage':
    global _action
    _action = _init_action.copy()
    _food.initialize(game_stage_layer)
    for game_button in _game_buttons:
        game_button.initialize(game_stage_layer)
    for game_image in _game_images:
        game_image.initialize(game_stage_layer)
    for game_text in _game_texts:
        game_text.initialize(game_stage_layer)
    tamagotchi.initialize(game_stage_layer)
    tamagotchi.animate_background_image(10)
    game_stage_layer.backgroundImage(_background_image_name)
    return GameStage(app, game_stage_layer)


class GameStage(StageBase):
    def __init__(self, app: DDAppBase, stage_layer: LayerGraphical):
        super().__init__(app, stage_layer, init_visible=False)
        self.start_time = None
        self.isSleep = False

    def startGame(self):
        self.start_time = time.time()

    def update(self):
        self.scoreTick()

    def handle_clicked(self, pos_x: int, pos_y: int):
        if _food.is_visible():
            if _food.check_clicked_cross(pos_x, pos_y):
                _food.set_visible(False)
        else:
            if not self.isSleep:
                if btn_satiety.check_clicked(pos_x, pos_y):
                    self.app.playButtonSound()
                    _food.set_visible(True)

    def scoreTick(self):
        t_time = time.time() - self.start_time
        if t_time > _timeout:
            _action['satiety'] -= 3
            _action['toilet'] -= 2
            _action['happy'] -= 3
            _action['health'] -= random.randint(0, 5)
            for game_text in _game_texts:
                game_text.update_text()
            self.start_time = time.time()
