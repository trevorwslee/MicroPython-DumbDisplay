# ***
# *** Adapted from SPACE SHOOTING/space_shooting_turtle.py of https://github.com/DimaGutierrez/Python-Games
# ***

import random
import time

from dumbdisplay.core import *
from dumbdisplay.layer_graphical import DDRootLayer, LayerGraphical
from dumbdisplay.layer_turtle import LayerTurtle
from dumbdisplay.layer_lcd import LayerLcd
from dumbdisplay.layer_joystick import LayerJoystick

from dumbdisplay_examples.utils import DDAppBase, create_example_wifi_dd


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

_fire_sound_file = "SS_missile.wav"
_explode_sound_file = "SS_explosion.wav"

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
    @staticmethod
    def distance(obj1: 'GameObject', obj2: 'GameObject') -> float:
        return ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) ** 0.5
    def __init__(self, layer: LayerGraphical, image_name: str, idx: int = 0):
        # if idx == 0:
        #     layer.cacheImageFromLocalFile(image_name, __file__)
        #     #layer.cacheImageFromLocalFile(image_name, folder_path=os.path.dirname(__file__))
        image_size = _image_sizes[image_name]
        level_id = f"{image_name}_{idx}"
        width = image_size[0]
        height = image_size[1]
        self.layer = layer
        #self.image_name = image_name
        self.level_id = level_id
        self.x: float = 0
        self.y: float = 0
        self._g_x: int = 0
        self._g_y: int = 0
        layer.addLevel(level_id, width, height, switch_to_it=True)
        #layer.drawImageFile(image_name, 0, 0)
        self._shape(image_name=image_name)
    def _shape(self, image_name: str):
        self.layer.switchLevel(self.level_id)
        self.layer.clear()
        self.layer.drawImageFile(image_name, 0, 0)
    def _setx(self, x: float):
        self._goto(x, self.y)
    def _sety(self, y: float):
        self._goto(self.x, y)
    def _goto(self, x: float, y: float):
        self.x = x
        self.y = y
        g_x = int(_to_g_x(x) + 0.5)
        g_y = int(_to_g_y(y) + 0.5)
        if self._g_x != g_x or self._g_y != g_y:
            self.layer.switchLevel(self.level_id)
            self.layer.setLevelAnchor(g_x, g_y)
            self._g_x = g_x
            self._g_y = g_y



class Player(GameObject):
    def __init__(self, layer: LayerGraphical):
        super().__init__(layer=layer, image_name=_player_image_name, idx=0)
        self.dy: float = 0
        self.dx: float = 0
        self.score: int = 0
        self.kills: int = 0
        self._goto(-350, 0)
    def set_move(self, speed_x: int, speed_y: int):
        if speed_x == 0:
            self.dx = 0
        else:
            self.dx = 0.45 * speed_x
            #self.dx = 1.75 * speed_x
        if speed_y == 0:
            self.dy = 0
        else:
            self.dy = -0.45 * speed_y
            #self.dy = -1.75 * speed_y
    def move(self):
        if self.dx == 0 and self.dy == 0:
            return
        x = self.x + self.dx
        y = self.y + self.dy
        if x < -380:
            x = -380
        elif x > -180:
            x = -180
        if y < -280:
            y = -280
        elif y > 280:
            y = 280
        self._goto(x, y)


class Missile(GameObject):
    def __init__(self, player: Player, layer: LayerGraphical, idx: int = 0):
        super().__init__(layer=layer, image_name=_missile_image_name, idx=idx)
        self.player = player
        self.dx: float = 0
        self.state = "ready"
        self._goto(0, 1000)
    def fire(self):
        player: Player = self.player
        self.state = "firing"
        self._goto(player.x, player.y)
        self.dx = 2.5
    def move(self):
        if self.state == "firing":
            x = self.x + self.dx
            if x != self.x:
                self._setx(x)
        if self.x > 400:
            self.state = "ready"
            self._sety(1000)


class Enemy(GameObject):
    def __init__(self, layer: LayerGraphical, idx: int = 0):
        super().__init__(layer=layer, image_name=_enemy_image_name, idx=idx)
        self.dx: float = random.randint(1, 5) / -3
        self.dy: float = 0
        self.max_health = random.randint(5, 15)
        self.health = self.max_health
        self._goto(random.randint(400, 480), random.randint(-280, 280))
    def enemy_respawn(self):
        self.dy = 0
        self._shape(image_name=_enemy_image_name)
        self.max_health = random.randint(5, 15)
        self.health = self.max_health
        #self.move()
    def boss_spawn(self):
        self._shape(image_name=_boss_image_name)
        self.max_health = 50
        self.health = self.max_health
        self.dy = random.randint(-5, 5) / 3
    def move(self):
        x = self.x + self.dx
        y = self.y + self.dy
        if x < -400:
            x = random.randint(400, 480)
            y = random.randint(-280, 280)
        elif y < -280:
            y = -280
            self.dy *= -1
        elif y > 280:
            y = 280
            self.dy *= -1
        self._goto(x, y)


class Star(GameObject):
    def __init__(self, layer: LayerGraphical, idx: int = 0):
        super().__init__(layer=layer, image_name=_star_image_name, idx=idx)
        self.dx = random.randint(1, 5) / -20
        self._goto(random.randint(-400, 400), random.randint(-290, 290))
    def move(self):
        x = self.x + self.dx
        y = self.y
        if self.x < -400:
            x = random.randint(400, 480)
            y = random.randint(-290, 290)
        self._goto(x, y)


class Pen:
    def __init__(self, dd: DumbDisplay, player: Player):
        pen_layer = LayerTurtle(dd, _width, _height)
        pen_layer.setTextFont("DL::Space", 24)
        pen_layer.penColor("azure")
        #pen_layer.rectangle(100, 200)
        self.layer: LayerTurtle = pen_layer
        self.player: Player = player
        self.recorded_score = None
        self.recorded_kills = None
    def draw_score(self):
        self.layer.goTo(-80, 270)
        #self.layer.write(f"Score: {player.score}  Kills: {player.kills}", font=("Comic sans", 16, "normal"))
        if (self.recorded_score is None or self.recorded_score != self.player.score) and (self.recorded_kills is None or self.recorded_kills != self.player.kills):
            self.recorded_score = self.player.score
            self.recorded_kills = self.player.kills
            self.layer.clear()
            self.layer.write(f"Score: {self.recorded_score}  Kills: {self.recorded_kills}")



class SpaceShootingApp(DDAppBase):
    def __init__(self, dd: DumbDisplay = create_example_wifi_dd()):
        super().__init__(dd)
        self.pen: Pen = None
        self.player: Player = None
        self.missiles: list[Missile] = None
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

        self.dd.backgroundColor("black")

        self.dd.cacheSoundBytesFromLocalFile(_fire_sound_file, __file__)
        self.dd.cacheSoundBytesFromLocalFile(_explode_sound_file, __file__)
        if False:
            self.dd.saveCachedSound(_fire_sound_file)
            self.dd.saveCachedSound(_explode_sound_file)

        game_objects_layer = LayerGraphical(self.dd, _width, _height)
        game_objects_layer.noBackgroundColor()
        #game_objects_layer.backgroundColor("black")
        game_objects_layer.border(3, "blue", "round", 1)

        game_objects_layer.cacheImageFromLocalFile(_player_image_name, __file__)
        game_objects_layer.cacheImageFromLocalFile(_enemy_image_name, __file__)
        game_objects_layer.cacheImageFromLocalFile(_star_image_name, __file__)
        game_objects_layer.cacheImageFromLocalFile(_missile_image_name, __file__)
        game_objects_layer.cacheImageFromLocalFile(_boss_image_name, __file__)

        player = Player(game_objects_layer)

        missiles: list[Missile] = []
        for idx in range(3):
            missile = Missile(player, game_objects_layer, idx)
            missiles.append(missile)

        enemies: list[Enemy] = []
        for idx in range(5):
            enemy = Enemy(game_objects_layer, idx)
            enemies.append(enemy)

        stars: list[Star] = []
        for idx in range(30):
            star = Star(game_objects_layer, idx)
            stars.append(star)

        pen = Pen(self.dd, player)

        joystick = LayerJoystick(self.dd)
        #joystick.border(20, "white")
        joystick.valueRange(-4, 4)
        joystick.snappy(True)
        #joystick.showValue(True)
        joystick.autoRecenter(True)
        joystick.moveToCenter()
        joystick.enableFeedback("", lambda layer, type, x, y, *args: self.handleJoystickFeedback(layer, type, x, y))

        fire_button = LayerLcd(self.dd, 2, 3, char_height=28)
        #fire_button.border(1, "darkred")
        fire_button.noBackgroundColor()
        fire_button.writeLine("🚀", 1)
        fire_button.enableFeedback("", lambda layer, type, x, y,  *args: self.handleFireButtonFeedback(layer, type, x, y))

        AutoPin('V',
                AutoPin('S'),
                AutoPin('H', joystick, AutoPinSpacer(5, 10), fire_button)).pin(self.dd)

        self.pen = pen
        self.player = player
        self.missiles = missiles
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
        for missile in self.missiles:
            missile.move()
        for star in self.stars:
            star.move()
        for enemy in self.enemies:
            enemy.move()
            for missile in self.missiles:
                if GameObject.distance(enemy, missile) < 20:
                    self.dd.playSound(_explode_sound_file)
                    #winsound.PlaySound("SS_explosion.wav",winsound.SND_ASYNC)
                    enemy.health -= 4
                    if enemy.health <= 0:
                        enemy._goto(random.randint(400, 480), random.randint(-280, 280))
                        self.player.kills += 1
                        if self.player.kills % 10 == 0:
                            enemy.boss_spawn()
                        else:
                            #enemy.boss_spawn()
                            enemy.enemy_respawn()
                    else:
                        enemy._setx(enemy.x + 20)
                    missile.dx = 0
                    missile._goto(0, 1000)
                    missile.state = "ready"
                    self.player.score += 10
        self.pen.draw_score()

    def handleJoystickFeedback(self, joystick, type: str, x: int, y: int):
        if type == "move":
            self.player.set_move(x, y)

    def handleFireButtonFeedback(self, fire_button: LayerLcd, type: str, x: int, y: int):
        if y == 1:
            for missile in self.missiles:
                if missile.state == "ready":
                    missile.fire()
                    print(f"* fire: x={x}, y={y}")
                    fire_button.flash()
                    self.dd.playSound(_fire_sound_file)
                    #winsound.PlaySound("SS_missile.wav",winsound.SND_ASYNC)
                    break

if __name__ == "__main__":
    from dumbdisplay_examples.utils import create_example_wifi_dd, DDAppBase
    app = SpaceShootingApp(create_example_wifi_dd())
    app.run()
