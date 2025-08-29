# ***
# *** Adapted from TETRIS ONE BLOCK\tetris_one_block.py of https://github.com/DimaGutierrez/Python-Games
# ***

import random
import time

from dumbdisplay.core import *
from dumbdisplay.layer_graphical import DDRootLayer
from dumbdisplay.layer_turtle import LayerTurtle
from dumbdisplay.layer_lcd import LayerLcd
from dumbdisplay_examples.tetris.tetris_common import Grid, _draw, _draw_grid, _width, _height, _colors, \
    _block_unit_width, _grid_n_rows, _grid_n_cols

from dumbdisplay_examples.utils import DDAppBase, create_example_wifi_dd

#_USE_LEVEL_ANCHOR_FOR_BLOCK = True
#_INIT_BLOCK_X = 5
_RANDOMIZE_ROW_COUNT = 1



# _width = 400
# _height = 700
# _top = 230
# _left = -110
# _block_unit_width = 20
# #_colors = ['black', 'red', 'lightblue', 'blue', 'orange', 'yellow', 'green', 'purple']
# _colors = ['black', 'crimson', 'cyan', 'ivory', 'coral', 'gold', 'lime', 'magenta']


_delay = 0.3  # For time/sleep
_grid = [  # 12x24
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
# _grid_n_cols = len(_grid[0])  # should be 12
# _grid_n_rows = len(_grid)     # should be 24


# class Grid:
#     def __init__(self):
#         if _RANDOMIZE_ROW_COUNT >= 0:
#             grid = []
#             for y in range(_grid_n_rows):
#                 grid_row = []
#                 for x in range(_grid_n_cols):
#                     if y >= (_grid_n_rows - _RANDOMIZE_ROW_COUNT) and random.random() < 0.7:
#                         color = random.randint(1, len(_colors) - 1)
#                     else:
#                         color = 0
#                     grid_row.append(color)
#                 grid.append(grid_row)
#             self.grid = grid
#         else:
#             self.grid = []
#             for grid_row in _grid:
#                 self.grid.append(grid_row.copy())
#         self.grid_dirty = []
#         for grid_row in self.grid:
#             grid_dirty_row = []
#             for cell in grid_row:
#                 dirty = True if cell != 0 else False
#                 grid_dirty_row.append(dirty)
#             self.grid_dirty.append(grid_dirty_row)
#         self.n_cols = _grid_n_cols
#         self.n_rows = _grid_n_rows
#
#     def check_reset_need_redraw(self, row_idx, col_idx):
#         dirty = self.grid_dirty[row_idx][col_idx]
#         if not dirty:
#             return False
#         self.grid_dirty[row_idx][col_idx] = False
#         return True
#
#     def get_value(self, row_idx, col_idx):
#         return self.grid[row_idx][col_idx]
#
#     def set_value(self, row_idx, col_idx, value):
#         if self.grid[row_idx][col_idx] != value:
#             self.grid[row_idx][col_idx] = value
#             self.grid_dirty[row_idx][col_idx] = True
#         # old_value = self.grid[row_idx][col_idx]
#         # self.grid[row_idx][col_idx] = value
#         # self.grid_dirty[row_idx][col_idx] = old_value != value
#
#


# def _calc_screen_position(x: int, y : int) -> (int, int):
#     screen_x = _left + (x * 20) # each turtle 20x20 pixels
#     screen_y = _top - (y * 20)
#     return (screen_x, screen_y)


def _create_grid() -> Grid:
    if _RANDOMIZE_ROW_COUNT >= 0:
        grid = []
        for y in range(_grid_n_rows):
            grid_row = []
            for x in range(_grid_n_cols):
                if y >= (_grid_n_rows - _RANDOMIZE_ROW_COUNT) and random.random() < 0.7:
                    color = random.randint(1, len(_colors) - 1)
                else:
                    color = 0
                grid_row.append(color)
            grid.append(grid_row)
    else:
        grid = []
        for grid_row in _grid:
            grid.append(grid_row.copy())
    return Grid(grid)


# def _draw(x, y, color_number, pen: LayerTurtle):
#     screen_x = _left + (x * _block_unit_width) # each turtle 20x20 pixels
#     screen_y = _top - (y * _block_unit_width)
#     # (screen_x, screen_y) = _calc_screen_position(x, y)
#     color = _colors[color_number]
#     pen.penColor(color)
#     pen.goTo(screen_x, screen_y, with_pen=False)
#     pen.rectangle(_block_unit_width - 2, _block_unit_width - 2, centered=True)
#
# # def _draw_block(block: 'Block', block_pen: LayerTurtle):
# #     block_pen.clear()
# #     _draw(block.x, block.y, block.color, block_pen)
#
# def _draw_grid(grid: Grid, pen: LayerTurtle):
#     for y in range(grid.n_rows):
#         for x in range(grid.n_cols):
#             if not grid.check_reset_need_redraw(y, x):
#                 continue
#             color_number = grid.get_value(y, x)
#             _draw(x, y, color_number, pen)



class Block:
    def __init__(self, x: int, y: int, block_pen: LayerTurtle):
        # self.x = _INIT_BLOCK_X
        # self.y = 0
        self.x = x
        self.y = y
        self.color = random.randint(1, len(_colors) - 1)
        self.block_pen = block_pen
        # if _USE_LEVEL_ANCHOR_FOR_BLOCK:
        #     self.block_pen.clear()
        #     _draw(self.x, self.y, self.color, self.block_pen)
        self.sync_image()

    def commit(self, grid: Grid):
        grid.set_value(self.y, self.x, self.color)
        if True:
            self.block_pen.clear()

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
        self.grid = _create_grid()
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
        if self.grid.get_value(y, x) != 0:
            #self.sync_image()
            return False
        self.block = Block(x, y, self.block_pen)
        self.sync_image()
        return True

    def commit_block(self):
        self.block.commit(self.grid)
        self.sync_image()
        self.block = None

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
        #self.resetBlock()


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
