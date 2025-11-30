# ***
# ***
# *** need a fast Python environment, specially for sending data to DD Android app
# *** if needed to, provide the command-line argument --no-sound to disable sound, which will be less demanding [on sending data to DD Android app]
# ***
# *** Adapted from https://github.com/YarikHrabovets/tamagotchi
# ***




import time

from dumbdisplay import *

from dumbdisplay_examples.utils import DDAppBase, create_example_wifi_dd


_RESOURCES_ID = "dumbdisplay_examples.tamagotchi"


_width = 800
_height = 500

_background_image_name = "background.jpg"

_cursor_image_name = "cursorHand_blue.png"
_cursor_width = 27
_cursor_height = 28
_cursor_level_id = "cursor"

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

class TamagotchiApp(DDAppBase):
    def __init__(self, dd: DumbDisplay, enable_sound: bool):
        super().__init__(dd)
        self.enable_sound = enable_sound
        self.stage_layer: LayerGraphical = None
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

        stage_layer = LayerGraphical(self.dd, _width, _height)
        stage_layer.noBackgroundColor()
        stage_layer.border(3, "darkgreen", "round", 1)
        # stage_layer.setTextSize(64)
        # stage_layer.setTextFont("DL::Roboto")
        # stage_layer.setTextColor("white")
        stage_layer.enableFeedback(":drag", lambda layer, type, x, y, *args: self.handleGameObjectsLayerFeedback(type, x, y))

        stage_layer.cacheImageFromLocalFile(_cursor_image_name, __file__)
        stage_layer.addLevel(_cursor_level_id, _cursor_width, _cursor_height, switch_to_it=True)
        stage_layer.setLevelAnchor(0, 0)
        stage_layer.drawImageFileFit(_cursor_image_name)

        buttons = [logika_label, start_btn, rule_btn, exit_btn]
        for button in buttons:
            stage_layer.cacheImageFromLocalFile(button.image_name, __file__)
            button._init_game_object_layer(stage_layer)

        stage_layer.cacheImageFromLocalFile(_background_image_name, __file__)
        stage_layer.backgroundImage(_background_image_name)

        self.stage_layer = stage_layer
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

    def handleGameObjectsLayerFeedback(self, type: str, x: int, y: int):
        print(f"handleGameObjectsLayerFeedback: type={type}, x={x}, y={y}")
        if x >= 0 and y >= 0:
            self.stage_layer.switchLevel(_cursor_level_id)
            self.stage_layer.setLevelAnchor(x, y)
        if type == "click":
            if logika_label.collidepoint(x, y):
                print("Logika label clicked")
            elif start_btn.collidepoint(x, y):
                print("Start button clicked")
            elif rule_btn.collidepoint(x, y):
                print("Help button clicked")
            elif exit_btn.collidepoint(x, y):
                print("Exit button clicked")
                self.masterReset()


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
