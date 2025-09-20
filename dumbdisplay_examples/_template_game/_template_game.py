# ***
# *** Adapted from SPACE SHOOTING/space_shooting_turtle.py of https://github.com/DimaGutierrez/Python-Games
# ***

import random
import time

from dumbdisplay.core import *
from dumbdisplay.layer_graphical import DDRootLayer
from dumbdisplay.layer_turtle import LayerTurtle
from dumbdisplay.layer_lcd import LayerLcd
from dumbdisplay_examples.tetris._common import Grid, _draw, _draw_grid, _width, _height, _colors, _grid_n_rows, _grid_n_cols

from dumbdisplay_examples.utils import DDAppBase, create_example_wifi_dd


_width = 800
_height = 600
_delay = 0.3

class TemplateGameApp(DDAppBase):
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

        root = DDRootLayer(self.dd, _width, _height)
        root.border(5, "darkred", "round", 1)
        root.backgroundColor("black")

        wn = LayerTurtle(self.dd, _width, _height)
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
        # left_button = LayerLcd(self.dd, 2, 1, char_height=28)
        # left_button.noBackgroundColor()
        # left_button.writeLine("⬅️")
        # left_button.enableFeedback("f", lambda *args: self.moveBlockLeft())
        #
        # right_button = LayerLcd(self.dd, 2, 1, char_height=28)
        # right_button.noBackgroundColor()
        # right_button.writeLine("➡️")
        # right_button.enableFeedback("f", lambda *args: self.moveBlockRight())

        # AutoPin('V',
        #         AutoPin('S'),
        #         AutoPin('H', left_button, right_button)).pin(self.dd)

        self.pen = wn

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


if __name__ == "__main__":
    from dumbdisplay_examples.utils import create_example_wifi_dd, DDAppBase
    app = TemplateGameApp(create_example_wifi_dd())
    app.run()
