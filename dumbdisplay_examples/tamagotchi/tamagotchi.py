import time

from dumbdisplay import *

from dumbdisplay_examples.utils import DDAppBase, create_example_wifi_dd


_RESOURCES_ID = "dumbdisplay_examples.tamagotchi"


_width = 800
_height = 500

_background_image_name = "background.jpg"
_toilet_sound_file = "toilet.ogg"

_delay = 0.1

class TamagotchiApp(DDAppBase):
    def __init__(self, dd: DumbDisplay = create_example_wifi_dd()):
        super().__init__(dd)
        self.wn: LayerTurtle = None
        self.last_update_time = None

    def initializeDD(self):

        game_objects_layer = LayerGraphical(self.dd, _width, _height)
        game_objects_layer.noBackgroundColor()
        game_objects_layer.border(3, "darkgreen", "round", 1)
        game_objects_layer.enableFeedback("", lambda layer, type, *args: self.handleGameObjectsLayerFeedback(type))

        game_objects_layer.cacheImageFromLocalFile(_background_image_name, __file__)

        game_objects_layer.backgroundImage(_background_image_name)


        if True:
            self.dd.cacheSoundBytesFromLocalFile(_toilet_sound_file, __file__, resources_id=_RESOURCES_ID)
            self.dd.playSound(_toilet_sound_file)
            self.dd.sleep(5)

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


if __name__ == "__main__":
    from dumbdisplay_examples.utils import create_example_wifi_dd, DDAppBase
    app = TamagotchiApp(create_example_wifi_dd())
    app.run()
