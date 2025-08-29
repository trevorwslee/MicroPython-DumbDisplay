# ***
# *** Adapted from TETRIS ONE BLOCK\tetris_one_block.py of https://github.com/DimaGutierrez/Python-Games
# ***

import random
import time

from dumbdisplay.core import *
from dumbdisplay.layer_graphical import DDRootLayer
from dumbdisplay.layer_turtle import LayerTurtle
from dumbdisplay.layer_lcd import LayerLcd
from dumbdisplay_examples.tetris.tetris_common import Grid, _colors, _grid_n_rows, _grid_n_cols, _block_unit_width, \
    _width, _height, _left, _top, _draw_grid, _check_can_place_block_grid, _commit_block_grid, Block

from dumbdisplay_examples.utils import DDAppBase, create_example_wifi_dd

_RANDOMIZE_ROW_COUNT = 2


# _width = 400
# _height = 700
# _top = 230
# _left = -110
# _block_unit_width = 20
# #_colors = ['black', 'red', 'lightblue', 'blue', 'orange', 'yellow', 'green', 'purple']
# _colors = ['black', 'crimson', 'cyan', 'ivory', 'coral', 'gold', 'lime', 'magenta']
# _grid_n_cols = 12
# _grid_n_rows = 24


_delay = 0.3  # For time/sleep

# class Grid:
#     def __init__(self, grid_cells):
#         self.grid_cells = grid_cells
#         self.grid_dirty = []
#         for grid_row in self.grid_cells:
#             grid_dirty_row = []
#             for cell in grid_row:
#                 dirty = True if cell != 0 else False
#                 grid_dirty_row.append(dirty)
#             self.grid_dirty.append(grid_dirty_row)
#         self.n_cols = len(self.grid_cells[0])
#         self.n_rows = len(self.grid_cells)
#
#     def check_reset_need_redraw(self, row_idx, col_idx):
#         dirty = self.grid_dirty[row_idx][col_idx]
#         if not dirty:
#             return False
#         self.grid_dirty[row_idx][col_idx] = False
#         return True
#
#     def get_value(self, row_idx, col_idx):
#         return self.grid_cells[row_idx][col_idx]
#
#     def set_value(self, row_idx, col_idx, value):
#         if self.grid_cells[row_idx][col_idx] != value:
#             self.grid_cells[row_idx][col_idx] = value
#             self.grid_dirty[row_idx][col_idx] = True


# def _draw(x, y, color_number, pen: LayerTurtle):
#     screen_x = _left + (x * _block_unit_width) # each turtle 20x20 pixels
#     screen_y = _top - (y * _block_unit_width)
#     # (screen_x, screen_y) = _calc_screen_position(x, y)
#     color = _colors[color_number]
#     pen.penColor(color)
#     pen.goTo(screen_x, screen_y, with_pen=False)
#     pen.rectangle(_block_unit_width - 2, _block_unit_width - 2, centered=True)


def _randomize_block_grid() -> Grid:
    color = random.randint(1, len(_colors) - 1)
    if True:
        n_rows = random.randint(1, 2)
        n_cols = random.randint(1, 2)
        block_grid = []
        for y in range(n_rows):
            block_grid_row = []
            for x in range(n_cols):
                block_grid_row.append(color)
            block_grid.append(block_grid_row)
    else:
        block_grid = [[color, color]]
    return Grid(grid_cells=block_grid)

def _randomize_grid() -> Grid:
    grid_cells = []
    for y in range(_grid_n_rows):
        grid_row = []
        for x in range(_grid_n_cols):
            if y >= (_grid_n_rows - _RANDOMIZE_ROW_COUNT) and random.random() < 0.7:
                color = random.randint(1, len(_colors) - 1)
            else:
                color = 0
            grid_row.append(color)
        grid_cells.append(grid_row)
    return Grid(grid_cells=grid_cells)

# def _check_can_place_block_grid(block_grid: Grid, block_grid_x_off: int, block_grid_y_offset: int, grid: Grid) -> bool:
#     for y in range(block_grid.n_rows):
#         for x in range(block_grid.n_cols):
#             if block_grid.get_value(y, x) != 0:
#                 row_idx = y + block_grid_y_offset
#                 col_idx = x + block_grid_x_off
#                 if row_idx < 0 or row_idx >= grid.n_rows:
#                     return True
#                 if col_idx < 0 or col_idx >= grid.n_cols:
#                     return True
#                 if grid.get_value(row_idx, col_idx) != 0:
#                     return True
#     return False
#
#
# def _commit_block_grid(block_grid: Grid, block_grid_x_off: int, block_grid_y_offset: int, grid: Grid):
#     for y in range(block_grid.n_rows):
#         for x in range(block_grid.n_cols):
#             color = block_grid.get_value(y, x)
#             if color != 0:
#                 grid.set_value(y + block_grid_y_offset, x + block_grid_x_off, color)


# def _draw(x, y, color_number, pen: LayerTurtle):
#     screen_x = _left + (x * _block_unit_width) # each turtle 20x20 pixels
#     screen_y = _top - (y * _block_unit_width)
#     # (screen_x, screen_y) = _calc_screen_position(x, y)
#     color = _colors[color_number]
#     pen.penColor(color)
#     pen.goTo(screen_x, screen_y, with_pen=False)
#     pen.rectangle(_block_unit_width - 2, _block_unit_width - 2, centered=True)
#
# def _draw_grid(grid: Grid, pen: LayerTurtle):
#     for y in range(grid.n_rows):
#         for x in range(grid.n_cols):
#             if not grid.check_reset_need_redraw(y, x):
#                 continue
#             color_number = grid.get_value(y, x)
#             _draw(x, y, color_number, pen)
#
#

# class Block:
#     def __init__(self, x: int, y: int, block_grid: Grid, block_pen: LayerTurtle):
#         self.x = x
#         self.y = y
#         self.block_grid = block_grid
#         self.block_pen = block_pen
#         block_pen.clear()
#         self.sync_image()
#         _draw_grid(block_grid, block_pen)
#
#     def move_down(self, grid: Grid) -> bool:
#         if _check_can_place_block_grid(self.block_grid, self.x, self.y + 1, grid=grid):
#             return False
#         self.y += 1
#         self.sync_image()
#         return True
#
#     def move_right(self, grid: Grid) -> bool:
#         if _check_can_place_block_grid(self.block_grid, self.x + 1, self.y, grid=grid):
#             return False
#         self.x += 1
#         self.sync_image()
#         return True
#
#     def move_left(self, grid: Grid) -> bool:
#         if _check_can_place_block_grid(self.block_grid, self.x - 1, self.y, grid=grid):
#             return False
#         self.x -= 1
#         self.sync_image()
#         return True
#
#     def sync_image(self):
#         #anchor_x = (self.x - _INIT_BLOCK_X) * _block_unit_width
#         anchor_x = self.x * _block_unit_width
#         anchor_y = self.y * _block_unit_width
#         self.block_pen.setLevelAnchor(anchor_x, anchor_y)



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
        self.grid = _randomize_grid()
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
        x -= 1 - block_grid.n_cols
        y -= 1 - block_grid.n_rows
        if _check_can_place_block_grid(block_grid, x, y, grid=self.grid):
            return False
        self.block = Block(x, y, block_grid=block_grid, block_pen=self.block_pen)
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
        border.write("Two-Block TETRIS", "C")

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
    app = TetrisTwoBlockApp(create_example_wifi_dd())
    app.run()
