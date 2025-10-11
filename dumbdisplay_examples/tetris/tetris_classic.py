# ***
# *** Adapted from TETRIS ONE BLOCK/tetris_one_block.py and TETRIS CLASSIC/tetris_turtle.py
# *** of https://github.com/DimaGutierrez/Python-Games
# *** - modified from dumbdisplay_examples/tetris/tetris_two_block.py
# ***

import time

from dumbdisplay.core import *
from dumbdisplay.layer_graphical import DDRootLayer
from dumbdisplay.layer_turtle import LayerTurtle
from dumbdisplay.layer_lcd import LayerLcd
from dumbdisplay_examples.tetris._common import  _width, _height, _draw_grid, _commit_block_grid, Block, \
    _check_bad_block_grid_placement, _randomize_grid
from dumbdisplay_examples.tetris._shapes import _randomize_block_grid

from dumbdisplay_examples.utils import DDAppBase, create_example_wifi_dd

_RANDOMIZE_ROW_COUNT = 2
_ROTATE_WITH_LEVEL = True


_delay = 0.5  # For time/sleep
_level_animation_millis = 50

def _check_grid(shape: 'Shape', score: LayerTurtle) -> (bool, int):
    grid = shape.grid
    block = shape.block

    # Check if each row is full:
    empty_count = 23
    deleted_count = 0
    for y in range(0,24):
        is_full = True
        is_empty = True
        y_erase = y
        for x in range(0,12):
            if grid.get_value(y, x) == 0:
                is_full = False
            else:
                is_empty = False
            if not is_empty and not is_full:
                empty_count -= 1
                break
        # Remove row and shift down
        if is_full:
            shape.score_count += 1
            score.clear()
            score.write(f'Score: {shape.score_count}', align='C')

            for y in range(y_erase-1, -1, -1):
                for x in range(0,12):
                    grid.set_value(y + 1, x, grid.get_value(y, x))

            deleted_count += 1

    return (empty_count == 23, deleted_count)


class Shape:
    def __init__(self, pen: LayerTurtle, block_pen: LayerTurtle):
        self.grid = _randomize_grid(_RANDOMIZE_ROW_COUNT)
        self.score_count = 0
        self.block: Block = None
        self.pen = pen
        self.block_pen = block_pen
        if not self.reset_block():
            raise Exception("Failed to create initial block")

    def check_grid(self, score: LayerTurtle) -> bool:
        (all_empty, delete_count) = _check_grid(self, score)
        if delete_count > 0:
            self.sync_image()
        return all_empty and self.block is None

    def reset_block(self) -> bool:
        x = 5
        y = 0
        block_grid = _randomize_block_grid()
        x -= int((block_grid.n_cols - 1) / 2)
        y += 1 - block_grid.n_rows
        if _check_bad_block_grid_placement(block_grid, x, y, grid=self.grid, check_boundary=False):
            return False
        self.block = Block(x, y, block_grid=block_grid, block_pen=self.block_pen, move_reach_in_millis=_level_animation_millis, classical_rotate_with_level=_ROTATE_WITH_LEVEL)
        self.sync_image()
        return True

    def commit_block(self):
        _commit_block_grid(self.block.block_grid, self.block.x, self.block.y, self.grid)
        #self.block.commit(self.grid)
        self.sync_image()
        self.block = None

    def move_block_down(self) -> bool:
        return self.block.move_down(self.grid)

    def move_block_right(self) -> bool:
        return self.block.move_right(self.grid)

    def rotate_block(self) -> bool:
        return self.block.rotate(self.grid)

    def move_block_left(self) -> bool:
        return self.block.move_left(self.grid)

    def sync_image(self):
        #self.block.sync_image()
        _draw_grid(self.grid, self.pen)


class TetrisTwoBlockApp(DDAppBase):
    def __init__(self, dd: DumbDisplay = create_example_wifi_dd()):
        super().__init__(dd)
        self.score: LayerTurtle = None
        self.block_pen: LayerTurtle = None
        self.pen: LayerTurtle = None
        self.shape: Shape = None
        self.last_update_time = None

    def initializeDD(self):

        root = DDRootLayer(self.dd, _width, _height)
        root.border(5, "darkred", "round", 1)
        root.backgroundColor("black")

        block_pen = LayerTurtle(self.dd, _width, _height)
        block_pen.penFilled()
        #block_pen.setTextSize(32)

        pen = LayerTurtle(self.dd, _width, _height)
        pen.penFilled()
        pen.setTextSize(32)

        score = LayerTurtle(self.dd, _width, _height)
        score.penColor('red')
        score.penUp()
        score.goTo(60, -300)
        score.setTextFont("Courier", 24)
        #score.write('Score: 0', 'C')

        border = LayerTurtle(self.dd, _width, _height)
        if False:
            border.rectangle(260, 490, centered=True)
        border.penSize(10)
        border.penUp()
        border.goTo(-130, 240)
        border.penDown()
        border.penColor('linen')
        border.rightTurn(90)
        border.forward(490) # Down
        border.leftTurn(90)
        border.forward(260) # Right
        border.leftTurn(90)
        border.forward(490) # Up
        border.penUp()
        border.goTo(0,260)
        border.setTextFont("Courier", 36)
        border.write("TETRIS", "C")

        left_button = LayerLcd(self.dd, 2, 1, char_height=28)
        left_button.noBackgroundColor()
        left_button.writeLine("⬅️")
        left_button.enableFeedback("f", lambda *args: self.moveBlockLeft())

        right_button = LayerLcd(self.dd, 2, 1, char_height=28)
        right_button.noBackgroundColor()
        right_button.writeLine("➡️")
        right_button.enableFeedback("f", lambda *args: self.moveBlockRight())

        rotate_button = LayerLcd(self.dd, 2, 1, char_height=28)
        rotate_button.noBackgroundColor()
        rotate_button.writeLine("🔄")
        rotate_button.enableFeedback("f", lambda *args: self.rotateBlock())

        AutoPin('V',
                AutoPin('S'),
                AutoPin('H', left_button, rotate_button, right_button)).pin(self.dd)

        self.score = score
        self.block_pen = block_pen
        self.pen = pen

        self.startGame()
        #self.shape = Shape()
        #self.resetBlock()

        self.last_update_time = time.time()

    def updateDD(self):
        now = time.time()
        need_update = (now - self.last_update_time) >= _delay
        if need_update:
            self.last_update_time = now
            self.update()

    def update(self):
        if self.shape is None:
            print("... waiting to restart ...")
            return

        moved_down = self.moveBlockDown()
        if not moved_down:
            self.shape.commit_block()
        won = self.checkGrid()
        if won:
            self.endGame(won=True)
        elif not moved_down:
            if not self.resetBlock():
                self.endGame(won=False)
            # if self.shape.block.y > 0:
            #     #self.shape.reset_block()
            #     self.resetBlock()
            # else:
            #     self.endGame(won=False)

    def startGame(self):
        self.score.clear()
        self.score.write('Score: 0', 'C')
        self.pen.clear()
        self.block_pen.clear()
        self.shape = Shape(pen=self.pen, block_pen=self.block_pen)
        print("... started game")


    def endGame(self, won: bool):
        #self.block_pen.clear()
        self.shape = None
        if won:
            msg = "🥳 YOU WON 🥳"
            color = "purple"
        else:
            msg = "GAME OVER 😔"
            color = "darkgray"
        self.pen.home(with_pen=False)
        self.pen.penColor("white")
        self.pen.oval(300, 100, centered=True)
        self.pen.penColor(color)
        self.pen.write(msg, align='C')
        print("... ended game")


    def checkGrid(self) -> bool:
        return self.shape.check_grid(score=self.score)
        # check_result = check_grid(shape=self.shape, score=self.score)
        # self.drawGrid()  # should only redraw if any lines were cleared
        # return check_result

    def resetBlock(self) -> bool:
        return self.shape.reset_block()
        #self.drawGrid()
        #self.drawBlock()

    def moveBlockDown(self) -> bool:
        return self.shape.move_block_down()
        # if self.shape.move_block_down():
        #     self.drawBlock()
        #     return True
        # return False

    def moveBlockLeft(self) -> bool:
        #print("$ move left")
        if self.shape is None:
            self.startGame()
            return False
        return self.shape.move_block_left()

    def moveBlockRight(self) -> bool:
        if self.shape is None:
            self.startGame()
            return False
        return self.shape.move_block_right()

    def rotateBlock(self) -> bool:
        if self.shape is None:
            self.startGame()
            return False
        return self.shape.rotate_block()

def run_tetris_classic():
    from dumbdisplay_examples.utils import create_example_wifi_dd
    print("*** Running TETRIS CLASSIC ***")
    app = TetrisTwoBlockApp(create_example_wifi_dd())
    app.run()

if __name__ == "__main__":
    run_tetris_classic()