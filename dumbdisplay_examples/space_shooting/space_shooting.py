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


# _width = 1000
# _height = 600
_width = 800
_height = 600
_half_width = _width // 2
_half_height = _height // 2
_delay = 0.015

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

def _to_g_x(x: float) -> float:
    return _half_width + x

def _to_g_y(y: float) -> float:
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
        self.x: float = 0
        self.y: float = 0
        self._g_x: int = 0
        self._g_y: int = 0
        layer.addLevel(level_id, width, height, switch_to_it=True)
        layer.drawImageFile(image_name, 0, 0)
    def _setx(self, x: float):
        self._goto(x, self.y)
    def _sety(self, y: float):
        self._goto(self.x, y)
    def _goto(self, x: float, y: float):
        self.x = x
        self.y = y
        g_x = _to_g_x(x)
        g_y = _to_g_y(y)
        self.layer.switchLevel(self.level_id)
        if self._g_x != g_x or self._g_y != g_y:
            self.layer.setLevelAnchor(g_x, g_y)
            self._g_x = g_x
            self._g_y = g_y


class Player(GameObject):
    def __init__(self, layer: LayerGraphical, image_name: str, idx: int = 0):
        super().__init__(layer=layer, image_name=image_name, idx=idx)
        self.dy: float = 0
        self.dx: float = 0
        self._goto(-350, 0)
    def up(self):
        self.dy = 1.75
    def down(self):
        self.dy = -1.75
    def move_left(self):
        self.dx = -1.75
    def move_right(self):
        self.dx = 1.75
    def move(self):
        if self.dx == 0 and self.dy == 0:
            return
        # self.sety(self.ycor() + self.dy)
        # self.setx(self.xcor() + self.dx)
        self._goto(self.x + self.dx, self.y + self.dy)
        # Check for border collisions
        if self.y > 280:
            self._sety(280)
            self.dy = 0
        elif self.y < -280:
            self._sety(-280)
            self.dy = 0
        if self.x < -380:
            self._setx(-380)
            self.dx = 0
        elif self.x > -180:
            self._setx(-180)
            self.dx = 0


class Enemy(GameObject):
    def __init__(self, layer: LayerGraphical, image_name: str, idx: int = 0):
        super().__init__(layer=layer, image_name=image_name, idx=idx)
        self.dx: float = random.randint(1, 5) / -3
        self.dy: float = 0
        self._goto(random.randint(400, 480), random.randint(-280, 280))
    def move(self):
        #self.setx(self.xcor() + self.dx)
        #self.sety(self.ycor() + self.dy)
        self._goto(self.x + self.dx, self.y + self.dy)
        # Border check
        if self.x < -400:
            self._goto(random.randint(400, 480), random.randint(-280, 280))
        # Check for border collision
        if self.y < -280:
            self._sety(-280)
            self.dy *= -1
        elif self.y > 280:
            self._sety(280)
            self.dy *= -1


class Star(GameObject):
    def __init__(self, layer: LayerGraphical, image_name: str, idx: int = 0):
        super().__init__(layer=layer, image_name=image_name, idx=idx)
        self.dx = random.randint(1, 5) / -20
        self._goto(random.randint(-400, 400), random.randint(-290, 290))
    def move(self):
        self._setx(self.x + self.dx)
        # Border check
        if self.x < -400:
            self._goto(random.randint(400, 480), random.randint(-290, 290))


class SpaceShootingApp(DDAppBase):
    def __init__(self, dd: DumbDisplay = create_example_wifi_dd()):
        super().__init__(dd)
        self.player: Player = None
        self.enemies: list[Enemy] = None
        self.stars: list[Star] = None
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

        enemies: list[Enemy] = []
        for idx in range(5):
            enemy = Enemy(game_object_layer, _enemy_image_name, idx)
            enemies.append(enemy)

        stars: list[Star] = []
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


        self.player = player
        self.enemies = enemies
        self.stars = stars
        self.last_update_time = time.time()

        self.startGame()


    def updateDD(self):
        now = time.time()
        need_update = (now - self.last_update_time) >= _delay
        if need_update:
            self.last_update_time = now
            self.update()

    def startGame(self):
        pass

    def update(self):
        self.player.move()
        # for missile in self.missiles:
        #     missile.move()
        #
        for star in self.stars:
            star.move()
        for enemy in self.enemies:
            enemy.move()

    def movePlayerLeft(self):
        self.player.move_left()

    def movePlayerRight(self):
        self.player.move_right()


if __name__ == "__main__":
    from dumbdisplay_examples.utils import create_example_wifi_dd, DDAppBase
    app = SpaceShootingApp(create_example_wifi_dd())
    app.run()
