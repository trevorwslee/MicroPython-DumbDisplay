from dumbdisplay import *
from dumbdisplay_examples.tamagotchi.common import Button, Panel, StageBase, LevelUIComponent, Image
from dumbdisplay_examples.utils import DDAppBase


_background_image_name = "background.jpg"


_info_satiety = Button(20, 30, 25, 50, "lightning.png")
_info_toilet = Button(150, 30, 50, 50, "toilet.png")
_info_happy = Button(270, 30, 50, 50, "smile.png")
_info_health = Button(30, 90, 60, 60, "health.png")

_day_image = Image(735, 70, 50, 50, "day.png")

btn_statistic = Button(715, 40, 150, 50, "buttonLong_brown.png", "Statistic")

btn_satiety = Button(85, 467, 150, 50, "buttonLong_brown.png", "Feed")
btn_toilet = Button(285, 467, 150, 50, "buttonLong_brown.png", "Clear")
btn_play = Button(515, 467, 150, 50, "buttonLong_brown.png", "Play")
btn_health = Button(715, 467, 150, 50, "buttonLong_brown.png", "Medicine")


_action = {'satiety': 100, 'toilet': 100, 'happy': 100, 'health': 100, 'logiki': 50}

class ActionText(LevelUIComponent):
    def __init__(self, x, y, action_key: str):
        super().__init__("acttxt", x, y, 50, 30)
        self.x = x
        self.y = y
        self.action_key = action_key
        self._drawn_text = None

    def initialize(self, stage_layer: LayerGraphical, init_visible: bool = True):
        super().initialize(stage_layer, init_visible)
        text_size = 24
        stage_layer.setTextSize(text_size)
        stage_layer.setTextFont("DL::Roboto")
        stage_layer.setTextColor("green")
        self.update_text()

    def update_text(self):
        text = _action[self.action_key].__str__()
        if text != self._drawn_text:
            self.stage_layer.pushLevelAndSwitchTo(self._level_id)
            self.stage_layer.drawTextLine(text)
            self.stage_layer.popLevel()
            self._drawn_text = text


_satiety_text = ActionText(40, 15, "satiety")
_toilet_text = ActionText(180, 15, "toilet")
_smile_text = ActionText(300, 15, "happy")
_health_text = ActionText(70, 75, "health")


_game_buttons = [_info_satiety, _info_toilet, _info_happy, _info_health,
                 btn_statistic,
                 btn_satiety, btn_toilet, btn_play, btn_health]
_game_images = [_day_image]
_game_texts = [_satiety_text, _toilet_text, _smile_text, _health_text]



def get_game_stage_image_names():
    image_names = [_background_image_name]
    for menu_button in _game_buttons:
        image_names.append(menu_button.image_name)
    for game_image in _game_images:
        image_names.append(game_image.image_name)
    return image_names


def setup_game_stage_layer(app: DDAppBase, game_stage_layer: LayerGraphical) -> 'GameStage':
    for game_button in _game_buttons:
        game_button.initialize(game_stage_layer)
    for game_image in _game_images:
        game_image.initialize(game_stage_layer)
    for game_text in _game_texts:
        game_text.initialize(game_stage_layer)
    game_stage_layer.backgroundImage(_background_image_name)
    return GameStage(app, game_stage_layer)


class GameStage(StageBase):
    def __init__(self, app: DDAppBase, stage_layer: LayerGraphical):
        super().__init__(app, stage_layer, init_visible=False)

    def handleClicked(self, pos_x: int,  pos_y: int):
        raise NotImplementedError("not implemented yet")
