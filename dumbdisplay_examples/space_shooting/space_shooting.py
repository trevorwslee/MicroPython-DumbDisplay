# ***
# ***
# *** need a fast Python environment, specially for sending data to DD Android app
# *** if needed to, provide the command-line argument --no-sound to disable sound, which will be less demanding [on sending data to DD Android app]
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

_missile_count = 3

_player_image_name = "player.png"
_enemy_image_name = "enemy.png"
_star_image_name = "red_star.png"
_star_small_image_name = "red_star_small.png"
_missile_image_name = "missile.png"
_boss_image_name = "boss.png"

_fire_sound_file = "SS_missile.wav"
_explode_sound_file = "SS_explosion.wav"

_image_sizes = {
    _player_image_name: (40, 31),
    _enemy_image_name: (30, 27),
    _star_image_name: (3, 3),
    _star_small_image_name: (3, 3),
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
        if True:
            obj1_g_l = _to_g_x(obj1.x)
            obj1_g_r = obj1_g_l + obj1.width
            obj1_g_t = _to_g_y(obj1.y)
            obj1_g_b = obj1_g_t + obj1.height
            obj2_g_l = _to_g_x(obj2.x)
            obj2_g_r = obj2_g_l + obj2.width
            obj2_g_t = _to_g_y(obj2.y)
            obj2_g_b = obj2_g_t + obj2.height
            # if rectangles intersect, distance is zero
            if not (obj1_g_r < obj2_g_l or obj1_g_l > obj2_g_r or obj1_g_b < obj2_g_t or obj1_g_t > obj2_g_b):
                return 0.0
            # otherwise, calculate the distance between the closest edges
            g_dx = max(obj2_g_l - obj1_g_r, obj1_g_l - obj2_g_r, 0)
            g_dy = max(obj2_g_t - obj1_g_b, obj1_g_t - obj2_g_b, 0)
            return (g_dx * g_dx + g_dy * g_dy) ** 0.5
        else:
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
        self.width: float = width
        self.height: float = height
        self.visible: bool = True
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
    def _set_visible(self,  visible: bool):
        self._goto(self.x, self.y, visible=visible)
    def _goto(self, x: float, y: float, visible: bool = True):
        self.x = x
        self.y = y
        g_x = int(_to_g_x(x) + 0.5)
        g_y = int(_to_g_y(y) + 0.5)
        if self.visible != visible:
            self.visible = visible
            self.layer.switchLevel(self.level_id)
            self.layer.levelTransparent(not self.visible)
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
        self.max_health = 5
        self.health = self.max_health
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
        super().__init__(layer=layer, image_name=_star_image_name if random.randint(0, 1) == 0 else _star_small_image_name, idx=idx)
        self.dx = random.randint(1, 5) / -20
        self._goto(random.randint(-400, 400), random.randint(-290, 290))
    def move(self):
        if not self.visible and random.randint(0, 40) == 0:
            self._set_visible(visible=True)
        if self.visible and random.randint(0, 120) == 0:
            self._set_visible(visible=False)
        if self.visible:
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
        self.recorded_health = None
    def draw_score(self, force: bool = False):
        if (force or self.recorded_score is None or self.recorded_score != self.player.score) or (self.recorded_kills is None or self.recorded_kills != self.player.kills) or (self.recorded_health is None or self.recorded_health != self.player.health):
            self.recorded_score = self.player.score
            self.recorded_kills = self.player.kills
            self.recorded_health = self.player.health
            self.layer.clear()
            self.layer.goTo(0, 270, with_pen=False)
            self.layer.write(f"Score: {self.recorded_score}  Kills: {self.recorded_kills}  Health: {self.player.health} ({(self.player.health/self.player.max_health):.0%})", align="C")



class SpaceShootingApp(DDAppBase):
    def __init__(self, dd: DumbDisplay = create_example_wifi_dd(), enable_sound: bool = True):
        super().__init__(dd)
        # self.initialized = False
        # self.pending_master_reset = False
        self.enable_sound = enable_sound
        self.pen: Pen = None
        self.player: Player = None
        self.missiles: list[Missile] = None
        self.enemies: list[Enemy] = None
        self.stars: list[Star] = None
        self.joystick: LayerJoystick = None
        self.fire_button: LayerLcd = None
        self.last_update_time = None
        self.recorded_missile_left: int = _missile_count
        self.game_paused: bool = False
        self.game_over: bool = False

    # def run(self):
    #     self.setup()
    #     while True:
    #         self.loop()
    # def setup(self):
    #     pass
    #
    # def loop(self):
    #     (connected, reconnecting) = self.dd.connectPassive()
    #     if connected:
    #         if not self.initialized:
    #             self.initializeDD()
    #             self.initialized = True
    #         elif reconnecting:
    #             self.dd.masterReset()
    #             self.initialized = False
    #         else:
    #             self.updateDD()
    #             if self.pending_master_reset:
    #                 self.dd.masterReset(keep_connected=True)
    #                 self.initialized = False
    #                 self.pending_master_reset = False


    def initializeDD(self):

        # root = DDRootLayer(self.dd, _width, _height + 180)
        # root.border(5, "darkred", "round", 1)
        # root.backgroundColor("black")
        #
        #wn = LayerTurtle(self.dd, _width, _height)
        #wn.rectangle(100, 200)

        self.dd.backgroundColor("black")

        if self.enable_sound:
            self.dd.cacheSoundBytesFromLocalFile(_fire_sound_file, __file__)
            self.dd.cacheSoundBytesFromLocalFile(_explode_sound_file, __file__)

        game_objects_layer = LayerGraphical(self.dd, _width, _height)
        game_objects_layer.noBackgroundColor()
        #game_objects_layer.backgroundColor("black")
        game_objects_layer.border(3, "blue", "round", 1)
        game_objects_layer.enableFeedback("", lambda layer, type, *args: self.handleGameObjectsLayerFeedback(type))

        game_objects_layer.cacheImageFromLocalFile(_player_image_name, __file__)
        game_objects_layer.cacheImageFromLocalFile(_enemy_image_name, __file__)
        game_objects_layer.cacheImageFromLocalFile(_star_image_name, __file__)
        game_objects_layer.cacheImageFromLocalFile(_star_small_image_name, __file__)
        game_objects_layer.cacheImageFromLocalFile(_missile_image_name, __file__)
        game_objects_layer.cacheImageFromLocalFile(_boss_image_name, __file__)

        self.dd.recordLayerSetupCommands()

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
        joystick.enableFeedback("", lambda layer, type, x, y, *args: self.handleJoystickFeedback(type, x, y))

        fire_button = LayerLcd(self.dd, 2, _missile_count, char_height=28)
        #fire_button.border(1, "darkred")
        fire_button.margin(5, 5, 20, 5)
        fire_button.noBackgroundColor()
        for i in range(_missile_count):
            fire_button.writeLine("🚀", y=i)
        fire_button.enableFeedback("", lambda *args: self.handleFireButtonFeedback())

        AutoPin('V',
                AutoPin('S'),
                AutoPin('H', joystick, AutoPinSpacer(16, 9), fire_button)).pin(self.dd)

        self.dd.playbackLayerCommands()

        self.pen = pen
        self.player = player
        self.missiles = missiles
        self.enemies = enemies
        self.stars = stars
        self.joystick = joystick
        self.fire_button = fire_button
        self.last_update_time = time.time()
        self.recorded_missile_left = _missile_count
        self.game_paused = False
        self.game_over = False
        #self.pending_master_reset = False

        print("* game initialized")


    def updateDD(self):
        now = time.time()
        need_update = (now - self.last_update_time) >= _delay
        if need_update:
            self.last_update_time = now
            self.update()

    def pauseGame(self):
        self.pen.layer.goTo(0, 0, with_pen=False)
        self.pen.layer.penColor("yellow")
        self.pen.layer.setTextSize(32)
        self.pen.layer.write("--- game paused --- ", align="C")
        self.pen.layer.goTo(0, -50, with_pen=False)
        self.pen.layer.penColor("white")
        self.pen.layer.setTextSize(24)
        self.pen.layer.write("double-press to continue", align="C")
        self.game_paused = True
        print("* game paused -- double-press to continue")

    def continueGame(self):
        self.game_paused = False
        self.pen.draw_score(force=True)
        print("* game continued")


    def endGame(self):
        self.pen.layer.goTo(0, 0, with_pen=False)
        self.pen.layer.penColor("yellow")
        self.pen.layer.setTextSize(32)
        self.pen.layer.write("*** GAME OVER ***", align="C")
        self.pen.layer.goTo(0, -50, with_pen=False)
        self.pen.layer.penColor("white")
        self.pen.layer.setTextSize(24)
        self.pen.layer.write("double-press to restart", align="C")
        self.game_over = True
        print("* game over -- double-press to restart")

    def restartGame(self):
        self.masterReset()
        print("* game restarted")


    def update(self):
        if self.game_paused or self.game_over:
            return
        self.player.move()
        detected_missile_count = 0
        for missile in self.missiles:
            missile.move()
            if missile.state == "ready":
                detected_missile_count += 1
        for star in self.stars:
            star.move()
        for enemy in self.enemies:
            enemy.move()
            for missile in self.missiles:
                if GameObject.distance(enemy, missile) < 1:  # was < 20
                    if self.enable_sound:
                        self.dd.playSound(_explode_sound_file)
                    #winsound.PlaySound("SS_explosion.wav",winsound.SND_ASYNC)
                    enemy.health -= 4
                    if enemy.health <= 0:
                        print("* you have killed an enemy")
                        enemy._goto(random.randint(400, 480), random.randint(-280, 280))
                        self.player.kills += 1
                        if self.player.kills % 10 == 0:
                            enemy.boss_spawn()
                        else:
                            enemy.enemy_respawn()
                            #enemy.boss_spawn()
                    else:
                        enemy._setx(enemy.x + 20)
                    missile.dx = 0
                    missile._goto(0, 1000)
                    missile.state = "ready"
                    #self.player.score += 10
                    self.player.score += enemy.max_health
            if GameObject.distance(enemy, self.player) < 1:  # was < 20
                print("* you have collided with an enemy")
                if self.enable_sound:
                    self.dd.playSound(_explode_sound_file)
                self.player._set_visible(visible=False)
                self.player.health -= 1 # random.randint(5, 10)
                enemy.health -= random.randint(5, 10)
                enemy._goto(random.randint(400, 480), random.randint(-280, 280))
                time.sleep(0.2)
                if self.enable_sound:
                    self.dd.playSound(_explode_sound_file)
                self.player._set_visible(visible=True)
                if self.player.health <= 0:
                    self.game_over = True
        delta_missile_left = detected_missile_count - self.recorded_missile_left
        if delta_missile_left != 0:
            if delta_missile_left < 0:
                for i in range(-delta_missile_left):
                    y =  (_missile_count - self.recorded_missile_left) + i
                    self.fire_button.writeLine("", y=y)
            else:
                for i in range(delta_missile_left):
                    y =  (_missile_count - self.recorded_missile_left) - i - 1
                    self.fire_button.writeLine("🚀", y=y)
            self.recorded_missile_left = detected_missile_count
        self.pen.draw_score()
        if self.game_over:
            self.endGame()


    def handleGameObjectsLayerFeedback(self, type: str):
        ##print("*** GameObjectsLayerFeedback:", type)
        if type == "doubleclick":
            if self.game_over:
               self.restartGame()
            else:
                if self.game_paused:
                    self.continueGame()
                else:
                    self.pauseGame()

    def handleJoystickFeedback(self, type: str, x: int, y: int):
        if self.game_paused or self.game_over:
            return
        if type == "move":
            self.player.set_move(x, y)

    def handleFireButtonFeedback(self):
        if self.game_paused or self.game_over:
            return
        for missile in self.missiles:
            if missile.state == "ready":
                missile.fire()
                #print(f"* fire: x={x}, y={y}")
                self.fire_button.flash()
                if self.game_paused:
                    self.dd.playSound(_fire_sound_file)
                break

if __name__ == "__main__":
    import sys
    from dumbdisplay_examples.utils import create_example_wifi_dd, DDAppBase
    args = sys.argv[1:]
    enable_sound = True
    if "--no-sound" in args:
        enable_sound = False
    app = SpaceShootingApp(create_example_wifi_dd(), enable_sound=enable_sound)
    app.run()
