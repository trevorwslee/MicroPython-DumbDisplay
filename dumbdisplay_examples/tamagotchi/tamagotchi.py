# ***
# ***
# *** need a fast Python environment, specially for sending data to DD Android app
# *** if needed to, provide the command-line argument --no-sound to disable sound, which will be less demanding [on sending data to DD Android app]
# ***
# *** Adapted from https://github.com/YarikHrabovets/tamagotchi
# ***

import time

from dumbdisplay import *
from dumbdisplay_examples.tamagotchi.game_stage import setup_game_stage_layer, GameStage, get_game_stage_image_names

from dumbdisplay_examples.utils import DDAppBase

from dumbdisplay_examples.tamagotchi.common import icon_cross_image_name, StageBase
from dumbdisplay_examples.tamagotchi.menu_stage import MenuStage, get_menu_stage_image_names, setup_menu_stage_layer


#from dumbdisplay_examples.tamagotchi.structs import *
#from dumbdisplay_examples.tamagotchi.menu_stage import *

_RESOURCES_ID = "dumbdisplay_examples.tamagotchi"


_width = 800
_height = 500


_cursor_image_name = "cursorHand_blue.png"
_cursor_width = 27
_cursor_height = 28
_cursor_level_id = "cursor"

# _help_panel_image_name = "panel_brown.png"
# _background_image_name = "background.jpg"

#_menu_sound_file = "menu.ogg"
_button_sound_file = "button.ogg"
_toilet_sound_file = "toilet.ogg"

_delay = 0.1

_sound_files = [_button_sound_file, _toilet_sound_file]

class TamagotchiApp(DDAppBase):
    def __init__(self, dd: DumbDisplay, enable_sound: bool):
        super().__init__(dd)
        self.mouse_direct = False
        self.enable_sound = enable_sound
        self.top_stage_layer: LayerGraphical = None
        #self.current_scene = None
        self.current_stage: StageBase = None
        self.menu_stage: MenuStage = None
        self.game_stage: GameStage = None
        self.pos_x = 0
        self.pos_y = 0
        self.mouse_coor = None
        self.last_update_time = None

    def initializeDD(self):
        # reset_game_stage()
        #
        if self.enable_sound:
            self.dd.log("* caching sounds ...")
            for sound_file in _sound_files:
                if True:
                    self.dd.log("* ... ... caching sound: " + sound_file)
                self.dd.cacheSoundBytesFromLocalFile(sound_file, __file__, resources_id=_RESOURCES_ID)
                #self.dd.playSound(sound_file)
            self.dd.log("* ... done caching sounds")

        image_names: set[str] = set()
        #image_names.update([_cursor_image_name, icon_cross_image_name])
        image_names.update([_cursor_image_name])
        image_names.update(get_menu_stage_image_names())
        image_names.update(get_game_stage_image_names())
        self.dd.log("* caching images ...")
        for image_name in image_names:
            if False:
                self.dd.log("* ... ... caching image: " + image_name)
            self.dd.cacheImageBytesFromLocalFile(image_name, __file__)
        self.dd.log("* ... done caching images")

        def _create_stage_layer(init_visible: bool = True) -> LayerGraphical:
            stage_layer = LayerGraphical(self.dd, _width, _height)
            stage_layer.border(3, "darkgreen", "round", 1)
            stage_layer.noBackgroundColor()
            if not init_visible:
                stage_layer.visibility(False)
            return stage_layer

        # create the layers in the correct order
        top_stage_layer = _create_stage_layer()   # for cursor
        menu_stage_layer = _create_stage_layer()
        game_stage_layer = _create_stage_layer(init_visible=False)

        # specific for top_stage_layer
        top_stage_layer.enableFeedback(":drag", lambda layer, ltp, x, y, *args: self.handleGameObjectsLayerFeedback(ltp, x, y))

        top_stage_layer.addLevel(_cursor_level_id, _cursor_width, _cursor_height, switch_to_it=True)
        top_stage_layer.setLevelAnchor(0, 0)
        top_stage_layer.drawImageFileFit(_cursor_image_name)

        menu_stage = setup_menu_stage_layer(app=self, menu_stage_layer=menu_stage_layer)
        game_stage = setup_game_stage_layer(app=self, game_stage_layer=game_stage_layer)

        self.top_stage_layer = top_stage_layer
        self.menu_stage = menu_stage
        self.game_stage = game_stage
        #self.current_scene = Scene.MENU
        self.current_stage = self.menu_stage

        self.last_update_time = time.time()

    def updateDD(self):
        now = time.time()
        need_update = (now - self.last_update_time) >= _delay
        if need_update:
            self.last_update_time = now
            self.update()

    def update(self):
        if self.current_stage is not None:
            self.current_stage.update()

    # def get_current_stage(self):
    #     if self.current_scene == Scene.MENU:
    #         return self.menu_stage
    #     if self.current_scene == Scene.GAME:
    #         return self.game_stage
    #     return None

    def playButtonSound(self):
        if self.enable_sound:
            self.dd.playSound(_button_sound_file)

    def handleStartGame(self):
        self.menu_stage.set_visible(visible=False)
        self.game_stage.set_visible(visible=True)
        #self.current_scene = Scene.GAME
        self.game_stage.startGame()
        self.current_stage = self.game_stage

    def handleGameObjectsLayerFeedback(self, ltp: str, x: int, y: int):
        move_cursor = False
        clicked = False
        if self.mouse_direct:
            print(f"handleGameObjectsLayerFeedback (DIRECT): type={ltp}, x={x}, y={y}")
            if x >= 0 and y >= 0:
                self.pos_x = x
                self.pos_y = y
                move_cursor = True
            if ltp == "click":
                clicked = True
        else:
            print(f"handleGameObjectsLayerFeedback: type={ltp}, x={x}, y={y}")
            if ltp == "doubleclick":
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
        # current_stage = self.get_current_stage()
        # if current_stage is not None:
        #     if clicked:
        #         current_stage.handleClicked(pos_x, pos_y)
        if clicked:
            self.current_stage.handle_clicked(pos_x, pos_y)


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
