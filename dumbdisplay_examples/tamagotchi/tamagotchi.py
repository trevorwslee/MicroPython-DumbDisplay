# ***
# ***
# *** need a fast Python environment, specially for sending data to DD Android app
# *** if needed to, provide the command-line argument --no-sound to disable sound, which will be less demanding [on sending data to DD Android app]
# ***
# *** Adapted from https://github.com/YarikHrabovets/tamagotchi
# ***




import time
from enum import Enum

from dumbdisplay import *

from dumbdisplay_examples.utils import DDAppBase, create_example_wifi_dd


_RESOURCES_ID = "dumbdisplay_examples.tamagotchi"


_width = 800
_height = 500


_cursor_image_name = "cursorHand_blue.png"
_cursor_width = 27
_cursor_height = 28
_cursor_level_id = "cursor"

_background_menu_0_image_name = "gifMenu-0.png"
_background_menu_1_image_name = "gifMenu-1.png"
_background_menu_image_name = "gifMenu-##0-1##.png"  # encoded for animation

_help_panel_image_name = "panel_brown.png"

_background_image_name = "background.jpg"

_menu_sound_file = "menu.ogg"
_toilet_sound_file = "toilet.ogg"

_delay = 0.1

_next_level_id = 1

class Button:
    def __init__(self, x: int, y:int , width: int, height: int, image_name: str, text: str = None):
        global _next_level_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_name = image_name
        self.text = text
        self.level_id = f"btn-{_next_level_id}"
        _next_level_id += _next_level_id

    def _init_game_object_layer(self, stage_layer: LayerGraphical):
        self.stage_layer = stage_layer
        stage_layer.addLevel(self.level_id, width=self.width, height=self.height, switch_to_it=True)
        stage_layer.setLevelAnchor(self.x, self.y)
        stage_layer.drawImageFileFit(self.image_name, 0, 0, self.width, self.height)
        #stage_layer.drawImageFileFit(self.image_name)
        if self.text is not None:
            stage_layer.setTextSize(32)
            stage_layer.setTextFont("DL::Roboto")
            stage_layer.setTextColor("white")
            stage_layer.drawTextLine(self.text, 0, align='C')

    def collidepoint(self, x, y):
        return (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)

        #self.image = pygame.transform.scale(pygame.image.load(path), (self.width, self.height))
        #self.normal_image = self.image
        #self.rect = self.image.get_rect(center=(self.x, self.y))

        #self.btn_text = pixel_font.render(self.text, True, (255, 255, 255))
        #self.btn_text_rect = self.btn_text.get_rect()
        #self.btn_text_rect.center = self.rect.center

    # def blit_btn(self):
    #     screen.blit(self.image, self.rect)
    #     screen.blit(self.btn_text, self.btn_text_rect)

    # def hover(self, x, y):
    #     if self.rect.collidepoint((x, y)):
    #         self.image = pygame.transform.scale(pygame.image.load(abs_path('images/sprites/buttonLong_blue.png')), (self.width, self.height))
    #     else:
    #         self.image = self.normal_image



logika_label = Button(70, 60, 100, 100, "logika.png")
start_btn = Button(140, 150, 200, 50, "buttonLong_brown.png", "Start")
rule_btn = Button(140, 250, 200, 50, "buttonLong_brown.png", "Help")
exit_btn = Button(140, 350, 200, 50, "buttonLong_brown.png", "Exit")


class Scene(Enum):
    MENU = 1


class StageBase:
    def __init__(self, app: 'TamagotchiApp', stage_layer: LayerGraphical):
        self.app = app
        self.stage_layer = stage_layer
    def handleClicked(self, pos_x: int,  pos_y: int):
        raise NotImplementedError()

class MenuStage(StageBase):
    def __init__(self, app: 'TamagotchiApp', stage_layer: LayerGraphical):
        super().__init__(app, stage_layer)
        self.endMenu = False
        #self.animCount = 0
        #self.start_time = None
    def handleClicked(self, pos_x: int,  pos_y: int):
        if logika_label.collidepoint(pos_x, pos_y):
            print("Logika label clicked")
        elif start_btn.collidepoint(pos_x, pos_y):
            print("Start button clicked")
        elif rule_btn.collidepoint(pos_x, pos_y):
            print("Help button clicked")
        elif exit_btn.collidepoint(pos_x, pos_y):
            print("Exit button clicked")
            self.app.masterReset()


class TamagotchiApp(DDAppBase):
    def __init__(self, dd: DumbDisplay, enable_sound: bool):
        super().__init__(dd)
        self.mouse_direct = False
        self.enable_sound = enable_sound
        self.top_stage_layer: LayerGraphical = None
        self.menu_stage: MenuStage = None
        self.pos_x = 0
        self.pos_y = 0
        self.mouse_coor = None
        self.last_update_time = None

    def initializeDD(self):
        menu_buttons = [logika_label, start_btn, rule_btn, exit_btn]

        if self.enable_sound:
            self.dd.log("* caching sounds ...")
            if True:
                self.dd.cacheSoundBytesFromLocalFile(_toilet_sound_file, __file__, resources_id=_RESOURCES_ID)
                #self.dd.playSound(_toilet_sound_file)
            else:
                self.dd.cacheSoundBytesFromLocalFile(_menu_sound_file, __file__, resources_id=_RESOURCES_ID)  # big ... background music
                #self.dd.playSound(_menu_sound_file)
            self.dd.log("* ... done caching sounds")

        self.dd.log("* caching images ...")
        self.dd.cacheImageFromLocalFile(_cursor_image_name, __file__)
        self.dd.cacheImageFromLocalFile(_background_menu_0_image_name, __file__)
        self.dd.cacheImageFromLocalFile(_background_menu_1_image_name, __file__)
        for menu_button in menu_buttons:
            self.dd.cacheImageFromLocalFile(menu_button.image_name, __file__)
        self.dd.log("* ... done caching images")


        # create the layers in the correct order
        top_stage_layer = LayerGraphical(self.dd, _width, _height)   # for cursor
        menu_stage_layer = LayerGraphical(self.dd, _width, _height)
        #background_layer = LayerGraphical(self.dd, _width, _height)  # for background

        # set the layer "decorations" to be the same (so that the coordinates match)
        top_stage_layer.border(3, "darkgreen", "round", 1)
        top_stage_layer.noBackgroundColor()
        menu_stage_layer.border(3, "darkgreen", "round", 1)
        menu_stage_layer.noBackgroundColor()
        #background_layer.border(3, "darkgreen", "round", 1)

        # specific for top_stage_layer
        # top_stage_layer.setTextSize(64)
        # top_stage_layer.setTextFont("DL::Roboto")
        # top_stage_layer.setTextColor("white")
        top_stage_layer.enableFeedback(":drag", lambda layer, type, x, y, *args: self.handleGameObjectsLayerFeedback(type, x, y))

        top_stage_layer.addLevel(_cursor_level_id, _cursor_width, _cursor_height, switch_to_it=True)
        top_stage_layer.setLevelAnchor(0, 0)
        top_stage_layer.drawImageFileFit(_cursor_image_name)

        # specific for menu_stage_layer
        for menu_button in menu_buttons:
            menu_button._init_game_object_layer(menu_stage_layer)
        menu_stage_layer.backgroundImage(_background_menu_image_name)
        menu_stage_layer.animateBackgroundImage(0.7)
        #menu_stage_layer.drawImageFile(background_menu_0_image_name)
        #menu_stage_layer.cacheImageFromLocalFile(_background_image_name, __file__)
        #menu_stage_layer.backgroundImage(_background_image_name)

        self.top_stage_layer = top_stage_layer

        self.menu_stage = MenuStage(self, menu_stage_layer)
        self.current_scene = Scene.MENU

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
        pass

    def get_current_stage(self):
        if self.current_scene == Scene.MENU:
            return self.menu_stage
        return None

    def handleGameObjectsLayerFeedback(self, type: str, x: int, y: int):
        move_cursor = False
        clicked = False
        if self.mouse_direct:
            print(f"handleGameObjectsLayerFeedback (DIRECT): type={type}, x={x}, y={y}")
            if x >= 0 and y >= 0:
                self.pos_x = x
                self.pos_y = y
                move_cursor = True
            if type == "click":
                clicked = True
        else:
            print(f"handleGameObjectsLayerFeedback: type={type}, x={x}, y={y}")
            if type == "doubleclick":
                self.pos_x = x
                self.pos_y = y
                move_cursor = True
                clicked = True
            else:
                if x >= 0 and y >= 0:
                    if self.mouse_coor is not None:
                        dx = x - self.mouse_coor[0]
                        dy = y - self.mouse_coor[1]
                        new_pos_x = self.pos_x + dx
                        new_pos_y = self.pos_y + dy
                        if new_pos_x < 0:
                            new_pos_x = 0
                        elif new_pos_x > _width:
                            new_pos_x = _width
                        if new_pos_y < 0:
                            new_pos_y = 0
                        elif new_pos_y > _height:
                            new_pos_y = _height
                        self.pos_x = new_pos_x
                        self.pos_y = new_pos_y
                        move_cursor = True
                    self.mouse_coor = (x, y)
                else:
                    self.mouse_coor = None
        pos_x = self.pos_x
        pos_y = self.pos_y
        if move_cursor:
            self.top_stage_layer.switchLevel(_cursor_level_id)
            self.top_stage_layer.setLevelAnchor(pos_x, pos_y)
        current_stage = self.get_current_stage()
        if current_stage is not None:
            if clicked:
                current_stage.handleClicked(pos_x, pos_y)


def run_tamagotchi():
    import sys
    args = sys.argv[1:]
    enable_sound = True
    if "--no-sound" in args:
        enable_sound = False
    print("*** Running TAMAGOTCHI ***")
    if not enable_sound:
        print("*** - sound is disabled")
    if DumbDisplay.runningWithMicropython():
        raise Exception("TAMAGOTCHI is not supported on MicroPython")
    from dumbdisplay.io_inet import io4Inet
    if enable_sound:
        send_buffer_size = 1024 * 1024  # 1 MB
        dd = DumbDisplay(io4Inet(send_buffer_size=send_buffer_size))
    else:
        dd = DumbDisplay(io4Inet())
    app = TamagotchiApp(dd, enable_sound=enable_sound)
    app.run()

if __name__ == "__main__":
    run_tamagotchi()
