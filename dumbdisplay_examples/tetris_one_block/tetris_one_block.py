# ***
# *** Adapted from TETRIS ONE BLOCK\tetris_one_block.py of https://github.com/DimaGutierrez/Python-Games
# ***
import random
import time

from dumbdisplay.core import *
from dumbdisplay.layer_graphical import DDRootLayer
from dumbdisplay.layer_turtle import LayerTurtle
from dumbdisplay.layer_lcd import LayerLcd

from dumbdisplay_examples.utils import DDAppBase, create_example_wifi_dd

_delay = 0.3  # For time/sleep
_grid = [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [4,3,3,1,0,1,0,3,3,4,0,1],
    [5,1,6,5,3,2,1,0,5,5,0,3],
    [1,2,3,4,5,2,0,4,2,3,0,4],
    [1,3,1,2,4,2,0,3,1,2,4,3],
    [1,1,2,3,0,2,2,2,0,3,0,1],
    [0,1,1,2,3,0,0,0,4,0,2,0],
    [2,0,1,2,3,0,6,5,5,5,0,2]
]

class Grid:
    def __init__(self):
        if True:
            self.grid = []
            for row in _grid:
                self.grid.append(row.copy())
        else:
            # debug
            self.grid = [[0 for _ in range(12)] for _ in range(24)]
            self.grid[23] = [2,0,1,2,3,0,6,5,5,5,0,2]
        self.grid_dirty = []
        for grid_row in self.grid:
            grid_dirty_row = []
            for cell in grid_row:
                dirty = True if cell != 0 else False
                grid_dirty_row.append(dirty)
            self.grid_dirty.append(grid_dirty_row)

    def check_reset_need_redraw(self, row_idx, col_idx):
        dirty = self.grid_dirty[row_idx][col_idx]
        if not dirty:
            return False
        self.grid_dirty[row_idx][col_idx] = False
        return True

    def get_value(self, row_idx, col_idx):
        return self.grid[row_idx][col_idx]

    def set_value(self, row_idx, col_idx, value):
        if self.grid[row_idx][col_idx] != value:
            self.grid[row_idx][col_idx] = value
            self.grid_dirty[row_idx][col_idx] = True
        # old_value = self.grid[row_idx][col_idx]
        # self.grid[row_idx][col_idx] = value
        # self.grid_dirty[row_idx][col_idx] = old_value != value



_top = 230
_left = -110
#_colors = ['black', 'red', 'lightblue', 'blue', 'orange', 'yellow', 'green', 'purple']
_colors = ['black', 'crimson', 'cyan', 'ivory', 'coral', 'gold', 'lime', 'magenta']


def _draw(x, y, color_number, pen: LayerTurtle):
    screen_x = _left + (x * 20) # each turtle 20x20 pixels
    screen_y = _top - (y * 20)
    color = _colors[color_number]
    pen.penColor(color)
    pen.goTo(screen_x, screen_y, with_pen=False)
    pen.rectangle(18, 18, centered=True)

# def _draw_block(block: 'Block', block_pen: LayerTurtle):
#     block_pen.clear()
#     _draw(block.x, block.y, block.color, block_pen)

def _draw_grid(grid: Grid, pen: LayerTurtle):
    for y in range(24):
        for x in range(12):
            if not grid.check_reset_need_redraw(y, x):
                continue
            color_number = grid.get_value(y, x)
            _draw(x, y, color_number, pen)



class Block:
    def __init__(self, block_pen: LayerTurtle):
        self.x = 5
        self.y = 0
        self.color = random.randint(1, 7)
        self.block_pen = block_pen

    def commit(self, grid: Grid):
        grid.set_value(self.y, self.x, self.color)

    def move_down(self, grid: Grid) -> bool:
        if self.y < 23 and grid.get_value(self.y + 1, self.x) == 0:
            self.y += 1
            self.sync_image()
            return True
        return False

    def move_right(self, grid: Grid) -> bool:
        if self.x < 11:
            if grid.get_value(self.y, self.x + 1) == 0:
                self.x += 1
                self.sync_image()
                return True
        return False

    def move_left(self, grid: Grid) -> bool:
        if self.x > 0:
            if grid.get_value(self.y, self.x - 1) == 0:
                self.x -= 1
                self.sync_image()
                return True
        return False

    def sync_image(self):
        self.block_pen.clear()
        _draw(self.x, self.y, self.color, self.block_pen)
        #_draw_block(self, self.block_pen)



def _check_grid(shape: 'Shape', score: LayerTurtle) -> bool:
    grid = shape.grid
    block = shape.block

    # Check if each row is full:
    empty_count = 23
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

    return empty_count == 23


class Shape:
    def __init__(self, pen: LayerTurtle, block_pen: LayerTurtle):
        self.grid = Grid()
        self.score_count = 0
        self.block: Block = None
        self.pen = pen
        self.block_pen = block_pen

    def check_grid(self, score: LayerTurtle) -> bool:
        return _check_grid(self, score)

    def reset_block(self):
        self.block = Block(self.block_pen)
        self.sync_image()
        #self.block.commit(self.grid)

    def commit_block(self):
        self.block.commit(self.grid)

    def move_block_down(self) -> bool:
        return self.block.move_down(self.grid)

    def move_block_right(self) -> bool:
        return self.block.move_right(self.grid)

    def move_block_left(self) -> bool:
        return self.block.move_left(self.grid)

    def sync_image(self):
        #self.block.sync_image()
        _draw_grid(self.grid, self.pen)


class TetrisOneBlockApp(DDAppBase):
    def __init__(self, dd: DumbDisplay = create_example_wifi_dd()):
        super().__init__(dd)
        self.score: LayerTurtle = None
        self.block_pen: LayerTurtle = None
        self.pen: LayerTurtle = None
        self.shape: Shape = None
        self.last_update_time = None

    def initializeDD(self):
        width = 400
        height = 700

        root = DDRootLayer(self.dd, width, height)
        root.border(5, "darkred", "round", 1)
        root.backgroundColor("black")

        block_pen = LayerTurtle(self.dd, width, height)
        block_pen.penFilled()
        block_pen.setTextSize(32)

        pen = LayerTurtle(self.dd, width, height)
        pen.penFilled()

        score = LayerTurtle(self.dd, width, height)
        score.penColor('red')
        score.penUp()
        score.goTo(60, -300)
        score.setTextFont("Courier", 24)
        #score.write('Score: 0', 'C')

        border = LayerTurtle(self.dd, width, height)
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
        border.write("One-Block TETRIS", "C")

        left_button = LayerLcd(self.dd, 2, 1, char_height=28)
        left_button.noBackgroundColor()
        left_button.writeLine("⬅️")
        left_button.enableFeedback("f", lambda *args: self.moveBlockLeft())

        right_button = LayerLcd(self.dd, 2, 1, char_height=28)
        right_button.noBackgroundColor()
        right_button.writeLine("➡️")
        right_button.enableFeedback("f", lambda *args: self.moveBlockRight())

        AutoPin('V',
                AutoPin('S'),
                AutoPin('H', left_button, right_button)).pin(self.dd)

        self.score = score
        self.block_pen = block_pen
        self.pen = pen

        self.startGame()
        #self.shape = Shape()
        #self.resetBlock()

    def updateDD(self):
        now = time.time()
        need_update = self.last_update_time is None or (now - self.last_update_time) >= _delay
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
            if self.shape.block.y > 0:
                #self.shape.reset_block()
                self.resetBlock()
            else:
                self.endGame(won=False)

    # def drawBlock(self):
    #     draw_block(block=self.shape.block, block_pen=self.block_pen)

    # def drawGrid(self):
    #     _draw_grid(grid=self.shape.grid, pen=self.pen)

    def startGame(self):
        self.score.clear()
        self.score.write('Score: 0', 'C')
        self.pen.clear()
        self.block_pen.clear()
        self.shape = Shape(pen=self.pen, block_pen=self.block_pen)
        self.resetBlock()


    def endGame(self, won: bool):
        self.block_pen.clear()
        self.shape = None
        if won:
            msg = "🥳 YOU WON 🥳"
            color = "purple"
        else:
            msg = "GAME OVER 😔"
            color = "darkgray"
        self.block_pen.home(with_pen=False)
        self.block_pen.penColor("white")
        self.block_pen.oval(300, 100, centered=True)
        self.block_pen.penColor(color)
        self.block_pen.write(msg, align='C')


    def checkGrid(self) -> bool:
        return self.shape.check_grid(score=self.score)
        # check_result = check_grid(shape=self.shape, score=self.score)
        # self.drawGrid()  # should only redraw if any lines were cleared
        # return check_result

    def resetBlock(self):
        self.shape.reset_block()
        #self.drawGrid()
        #self.drawBlock()

    def moveBlockDown(self) -> bool:
        return self.shape.move_block_down()
        # if self.shape.move_block_down():
        #     self.drawBlock()
        #     return True
        # return False

    def moveBlockLeft(self) -> bool:
        if self.shape is None:
            self.startGame()
            return False
        return self.shape.move_block_left()
        # if self.shape.move_block_left():
        #     self.drawBlock()
        #     return True
        # return False

    def moveBlockRight(self) -> bool:
        if self.shape is None:
            self.startGame()
            return False
        return self.shape.move_block_right()
        # if self.shape.move_block_right():
        #     self.drawBlock()
        #     return True
        # return False


if __name__ == "__main__":
    from dumbdisplay_examples.utils import create_example_wifi_dd, DDAppBase
    app = TetrisOneBlockApp(create_example_wifi_dd())
    app.run()
