# ***
# *** Adapted from SPACE SHOOTING/space_shooting_turtle.py of https://github.com/DimaGutierrez/Python-Games
# ***

import random
import time

from dumbdisplay.core import *
from dumbdisplay.layer_graphical import DDRootLayer, LayerGraphical
from dumbdisplay.layer_turtle import LayerTurtle
from dumbdisplay.layer_lcd import LayerLcd
from dumbdisplay_examples.tetris._common import Grid, _draw, _draw_grid, _width, _height, _colors, _grid_n_rows, _grid_n_cols

from dumbdisplay_examples.utils import DDAppBase, create_example_wifi_dd


_width = 1000
_height = 600
_half_width = _width // 2
_half_height = _height // 2
_delay = 0.3

_player_image_name = "player.png"
_enemy_image_name = "enemy.png"
_star_image_name = "red_star.png"
_missile_image_name = "missile.png"
_boss_image_name = "boss.png"

_image_sizes = {
    _player_image_name: (40, 31),
    _enemy_image_name: (30, 27),
    _star_image_name: (3, 3),
    _missile_image_name: (20, 5),
    _boss_image_name: (30, 27),
}

def _to_graphical_x(x: int) -> int:
    return _half_width + x

def _to_graphical_y(y: int) -> int:
    return _half_height - y

class GameObject:
    def __init__(self, layer: LayerGraphical, image_name: str, idx: int = 0):
        if idx == 0:
            layer.cacheImageFromLocalFile(image_name)
        image_size = _image_sizes[image_name]
        level_id = f"{image_name}_{idx}"
        width = image_size[0]
        height = image_size[1]
        self.layer = layer
        self.image_name = image_name
        self.level_id = level_id
        self.x = 0
        self.y = 0
        layer.addLevel(level_id, width, height, switch_to_it=True)
        layer.drawImageFile(image_name, 0, 0)
    def _move_to(self, tt_x: int, tt_y: int):
        self.x = _to_graphical_x(tt_x)
        self.y = _to_graphical_y(tt_y)
        self.layer.switchLevel(self.level_id)
        self.layer.setLevelAnchor(self.x, self.y)


class Player(GameObject):
    def __init__(self, layer: LayerGraphical, image_name: str, idx: int = 0):
        super().__init__(layer=layer, image_name=image_name, idx=idx)
        self.dy = 0
        self.dx = 0
        self._move_to(350, 0)

class Enemy(GameObject):
    def __init__(self, layer: LayerGraphical, image_name: str, idx: int = 0):
        super().__init__(layer=layer, image_name=image_name, idx=idx)
        self.dx = random.randint(1, 5) / -3
        self.dy = 0
        self._move_to(random.randint(400, 480), random.randint(-280, 280))

class Star(GameObject):
    def __init__(self, layer: LayerGraphical, image_name: str, idx: int = 0):
        super().__init__(layer=layer, image_name=image_name, idx=idx)
        self.dx = random.randint(1, 5) / -20
        self._move_to(random.randint(-400, 400), random.randint(-290, 290))



class SpaceShootingApp(DDAppBase):
    def __init__(self, dd: DumbDisplay = create_example_wifi_dd()):
        super().__init__(dd)
        self.wn: LayerTurtle = None
        self.last_update_time = None

    def run(self):
        self.setup()
        while True:
            self.loop()
    def setup(self):
        pass

    def loop(self):
        (connected, reconnecting) = self.dd.connectPassive()
        if connected:
            if not self.initialized:
                self.initializeDD()
                self.initialized = True
            elif reconnecting:
                self.dd.masterReset()
                self.initialized = False
            else:
                self.updateDD()


    def initializeDD(self):

        # root = DDRootLayer(self.dd, _width, _height + 180)
        # root.border(5, "darkred", "round", 1)
        # root.backgroundColor("black")
        #
        #wn = LayerTurtle(self.dd, _width, _height)
        #wn.rectangle(100, 200)

        game_object_layer = LayerGraphical(self.dd, _width, _height)
        game_object_layer.backgroundColor("black")
        #game_object_layer.border(5, "red")

        player = Player(game_object_layer, _player_image_name)

        enemies = []
        for idx in range(5):
            enemy = Enemy(game_object_layer, _enemy_image_name, idx)
            enemies.append(enemy)

        stars = []
        for idx in range(30):
            star = Star(game_object_layer, _star_image_name, idx)
            stars.append(star)


        # for image_idx in range(len(_all_image_names)):
        #     game_object = GameObject(game_object_layer, image_idx)
        #     #game_object_layer.cacheImageFromLocalFile(image_name)
        #     #game_object_layer.saveCachedImageFile(image_name)
        #     #game_object_layer.drawImageFileFit(image_name)

        #
        # block_pen = LayerTurtle(self.dd, _width, _height)
        # block_pen.penFilled()
        # #block_pen.setTextSize(32)
        #
        # pen = LayerTurtle(self.dd, _width, _height)
        # pen.penFilled()
        # pen.setTextSize(32)
        #
        # score = LayerTurtle(self.dd, _width, _height)
        # score.penColor('red')
        # score.penUp()
        # score.goTo(60, -300)
        # score.setTextFont("Courier", 24)
        # #score.write('Score: 0', 'C')
        #
        # border = LayerTurtle(self.dd, _width, _height)
        # if False:
        #     border.rectangle(260, 490, centered=True)
        # border.penSize(10)
        # border.penUp()
        # border.goTo(-130, 240)
        # border.penDown()
        # border.penColor('linen')
        # border.rightTurn(90)
        # border.forward(490) # Down
        # border.leftTurn(90)
        # border.forward(260) # Right
        # border.leftTurn(90)
        # border.forward(490) # Up
        # border.penUp()
        # border.goTo(0,260)
        # border.setTextFont("Courier", 36)
        # border.write("One-Block TETRIS", "C")
        #
        left_button = LayerLcd(self.dd, 2, 1, char_height=28)
        left_button.noBackgroundColor()
        left_button.writeLine("⬅️")
        left_button.enableFeedback("f", lambda *args: self.movePlayerLeft())
        #
        right_button = LayerLcd(self.dd, 2, 1, char_height=28)
        right_button.noBackgroundColor()
        right_button.writeLine("➡️")
        right_button.enableFeedback("f", lambda *args: self.movePlayerRight())

        AutoPin('V',
                AutoPin('S'),
                AutoPin('H', left_button, AutoPinSpacer(width=400, height=100), right_button)).pin(self.dd)

        #self.pen = wn

        self.startGame()

        self.last_update_time = time.time()

    def updateDD(self):
        now = time.time()
        need_update = (now - self.last_update_time) >= _delay
        if need_update:
            self.last_update_time = now
            self.update()

    def startGame(self):
        pass

    def update(self):
        pass

    def movePlayerLeft(self):
        pass

    def movePlayerRight(self):
        pass


if __name__ == "__main__":
    from dumbdisplay_examples.utils import create_example_wifi_dd, DDAppBase
    app = SpaceShootingApp(create_example_wifi_dd())
    app.run()
