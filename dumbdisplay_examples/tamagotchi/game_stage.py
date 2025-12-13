from dumbdisplay import *
from dumbdisplay_examples.tamagotchi.common import Button, Panel, StageBase
from dumbdisplay_examples.utils import DDAppBase


_background_image_name = "background.jpg"


_info_satiety = Button(20, 30, 25, 50, "lightning.png")
_info_toilet = Button(150, 30, 50, 50, "toilet.png")
_info_happy = Button(270, 30, 50, 50, "smile.png")
_info_health = Button(30, 90, 60, 60, "health.png")

btn_statistic = Button(715, 40, 150, 50, "buttonLong_brown.png", "Statistic")

btn_satiety = Button(85, 467, 150, 50, "buttonLong_brown.png", "Feed")
btn_toilet = Button(285, 467, 150, 50, "buttonLong_brown.png", "Clear")
btn_play = Button(515, 467, 150, 50, "buttonLong_brown.png", "Play")
btn_health = Button(715, 467, 150, 50, "buttonLong_brown.png", "Medicine")


_game_buttons = [_info_satiety, _info_toilet, _info_happy, _info_health,
 btn_statistic,
 btn_satiety, btn_toilet, btn_play, btn_health]

def get_game_stage_image_names():
    image_names = [_background_image_name]
    for menu_button in _game_buttons:
        image_names.append(menu_button.image_name)
    return image_names


def setup_game_stage_layer(app: DDAppBase, game_stage_layer: LayerGraphical) -> 'GameStage':
    for game_button in _game_buttons:
        game_button.initialize(game_stage_layer)
    game_stage_layer.backgroundImage(_background_image_name)
    return GameStage(app, game_stage_layer)


class GameStage(StageBase):
    def __init__(self, app: DDAppBase, stage_layer: LayerGraphical):
        super().__init__(app, stage_layer, init_visible=False)

    def handleClicked(self, pos_x: int,  pos_y: int):
        raise NotImplementedError("not implemented yet")
