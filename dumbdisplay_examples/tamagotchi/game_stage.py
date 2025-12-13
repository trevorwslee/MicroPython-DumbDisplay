from dumbdisplay import *
from dumbdisplay_examples.tamagotchi.common import Button, Panel, StageBase
from dumbdisplay_examples.utils import DDAppBase


_background_image_name = "background.jpg"


def get_game_stage_image_names():
    image_names = [_background_image_name]
    return image_names


def setup_game_stage_layer(app: DDAppBase, game_stage_layer: LayerGraphical) -> 'GameStage':
    game_stage_layer.backgroundImage(_background_image_name)
    return GameStage(app, game_stage_layer)


class GameStage(StageBase):
    def __init__(self, app: DDAppBase, stage_layer: LayerGraphical):
        super().__init__(app, stage_layer, init_visible=False)

    def handleClicked(self, pos_x: int,  pos_y: int):
        raise NotImplementedError("not implemented yet")
