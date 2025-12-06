# ***
# ***
# *** need a fast Python environment, specially for sending data to DD Android app
# *** if needed to, provide the command-line argument --no-sound to disable sound, which will be less demanding [on sending data to DD Android app]
# ***
# *** Adapted from https://github.com/YarikHrabovets/tamagotchi
# ***

import time

from dumbdisplay import *

from dumbdisplay_examples.utils import DDAppBase

from dumbdisplay_examples.tamagotchi.structs import Scene
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

_menu_sound_file = "menu.ogg"
_toilet_sound_file = "toilet.ogg"

_delay = 0.1


class TamagotchiApp(DDAppBase):
    def __init__(self, dd: DumbDisplay, enable_sound: bool):
        super().__init__(dd)
        self.mouse_direct = False
        self.enable_sound = enable_sound
        self.top_stage_layer: LayerGraphical = None
        self.current_scene = None
        self.menu_stage: MenuStage = None
        self.pos_x = 0
        self.pos_y = 0
        self.mouse_coor = None
        self.last_update_time = None

    def initializeDD(self):
        if self.enable_sound:
            self.dd.log("* caching sounds ...")
            if True:
                self.dd.cacheSoundBytesFromLocalFile(_toilet_sound_file, __file__, resources_id=_RESOURCES_ID)
                #self.dd.playSound(_toilet_sound_file)
            else:
                self.dd.cacheSoundBytesFromLocalFile(_menu_sound_file, __file__, resources_id=_RESOURCES_ID)  # big ... background music
                #self.dd.playSound(_menu_sound_file)
            self.dd.log("* ... done caching sounds")

        image_names = [_cursor_image_name]
        image_names += get_menu_stage_image_names()
        self.dd.log("* caching images ...")
        for image_name in image_names:
            self.dd.cacheImageBytesFromLocalFile(image_name, __file__)
        self.dd.log("* ... done caching images")

        # create the layers in the correct order
        top_stage_layer = LayerGraphical(self.dd, _width, _height)   # for cursor
        menu_stage_layer = LayerGraphical(self.dd, _width, _height)

        # set the layer "decorations" to be the same (so that the coordinates match)
        top_stage_layer.border(3, "darkgreen", "round", 1)
        top_stage_layer.noBackgroundColor()
        menu_stage_layer.border(3, "darkgreen", "round", 1)
        menu_stage_layer.noBackgroundColor()

        # specific for top_stage_layer
        top_stage_layer.enableFeedback(":drag", lambda layer, ltp, x, y, *args: self.handleGameObjectsLayerFeedback(ltp, x, y))

        top_stage_layer.addLevel(_cursor_level_id, _cursor_width, _cursor_height, switch_to_it=True)
        top_stage_layer.setLevelAnchor(0, 0)
        top_stage_layer.drawImageFileFit(_cursor_image_name)

        # specific for menu_stage_layer
        setup_menu_stage_layer(menu_stage_layer=menu_stage_layer)

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
