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

class GridRow:
    def __init__(self, grid, grid_dirty):
        self.grid = grid
        self.grid_dirty = grid_dirty
        self.row_idx = 0
    def __len__(self):
        return len(self.grid[self.row_idx])
    def __getitem__(self, col_idx):
        return self.grid[self.row_idx][col_idx]
    def __setitem__(self, col_idx, value):
        self.grid[self.row_idx][col_idx] = value
        self.grid_dirty[self.row_idx][col_idx] = True

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
        self.grid_row = GridRow(self.grid, self.grid_dirty)
    def __len__(self):
        return len(self.grid)
    def __getitem__(self, row_idx):
        self.grid_row.row_idx = row_idx
        return self.grid_row
    def check_reset_need_redraw(self, row_idx, col_idx):
        dirty = self.grid_dirty[row_idx][col_idx]
        if not dirty:
            return False
        self.grid_dirty[row_idx][col_idx] = False
        return True

class Block:
    def __init__(self):
        self.x = 5
        self.y = 0
        self.color = random.randint(1, 7)

    def commit(self, grid):
        grid[self.y][self.x] = self.color

    def move_down(self, grid) -> bool:
        if self.y < 23 and grid[self.y + 1][self.x] == 0:
            grid[self.y][self.x]=0
            self.y += 1
            grid[self.y][self.x] = self.color
            return True
        return False

    def move_right(self, grid) -> bool:
        if self.x < 11:
            if grid[self.y][self.x + 1]==0:
                grid[self.y][self.x]=0
                self.x += 1
                grid[self.y][self.x] = self.color
                return True
        return False

    def move_left(self, grid) -> bool:
        if self.x > 0:
            if grid[self.y][self.x - 1]==0:
                grid[self.y][self.x]=0
                self.x -= 1
                grid[self.y][self.x] = self.color
                return True
        return False


class Shape:
    def __init__(self):
        self.grid = Grid()
        self.score_count = 0
        self.block: Block = None
        self.reset()

    def reset(self):
        self.block = Block()
        self.block.commit(self.grid)

    def move_down(self) -> bool:
        return self.block.move_down(self.grid)

    def move_right(self) -> bool:
        return self.block.move_right(self.grid)

    def move_left(self) -> bool:
        return self.block.move_left(self.grid)


def draw_grid(shape: Shape, pen: LayerTurtle):
    grid = shape.grid

    #pen.clear()
    top = 230
    left = -110
    colors = ['black', 'red', 'lightblue', 'blue', 'orange', 'yellow', 'green',
              'purple']

    for y in range(len(grid)): # 24 rows
        for x in range(len(grid[0])): # 12 columns
            if not grid.check_reset_need_redraw(y, x):
                continue
            screen_x = left + (x*20) # each turtle 20x20 pixels
            screen_y = top - (y*20)
            color_number = grid[y][x]
            color = colors[color_number]
            pen.penColor(color)
            pen.goTo(screen_x, screen_y, with_pen=False)
            #self.pen.stamp()
            pen.rectangle(18, 18, centered=True)


def check_grid(shape: Shape, score: LayerTurtle) -> bool:
    grid = shape.grid

    # Check if each row is full:
    empty_count = 23
    for y in range(0,24):
        is_full = True
        is_empty = True
        y_erase = y
        for x in range(0,12):
            if grid[y][x] == 0:
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
                    grid[y + 1][x] = grid[y][x]

    return empty_count == 23



class TetrisOneBlockApp(DDAppBase):
    def __init__(self, dd: DumbDisplay = create_example_wifi_dd()):
        super().__init__(dd)
        # self.root: DDRootLayer = None
        self.score: LayerTurtle = None
        self.pen: LayerTurtle = None
        # self.left_button: LayerLcd = None
        # self.right_button: LayerLcd = None
        self.shape: Shape = None
        self.last_update_time = None

    def initializeDD(self):
        width = 400
        height = 700

        root = DDRootLayer(self.dd, width, height)
        root.border(5, "darkred", "round", 1)
        root.backgroundColor("black")

        score = LayerTurtle(self.dd, width, height)
        score.penColor('red')
        score.penUp()
        #score.hideturtle()
        score.goTo(60, -300)
        #score.write('Score: 0', align='center', font=('Courier', 24, 'normal'))
        score.setTextFont("Courier", 24)
        score.write('Score: 0', 'C')

        border = LayerTurtle(self.dd, width, height)
        border.penSize(10)
        border.penUp()
        #border.hideturtle()
        border.goTo(-130, 240)
        border.penDown()
        border.penColor('white')
        border.rightTurn(90)
        border.forward(490) # Down
        border.leftTurn(90)
        border.forward(260) # Right
        border.leftTurn(90)
        border.forward(490) # Up
        border.penUp()
        border.goTo(0,260)
        #border.write("TETRIS", align='center', font=('Courier', 36, 'normal'))
        border.setTextFont("Courier", 36)
        border.write("TETRIS (one block)", "C")

        pen = LayerTurtle(self.dd, width, height)
        #pen.up()
        # pen.speed(0)
        # pen.shape('square')
        # pen.shapesize(0.9, 0.9)
        # pen.setundobuffer(None)
        pen.penFilled()

        left_button = LayerLcd(self.dd, 2, 1, char_height=28)
        left_button.noBackgroundColor()
        left_button.writeLine("⬅️")
        left_button.enableFeedback("f", lambda *args: self.moveShapeLeft())

        right_button = LayerLcd(self.dd, 2, 1, char_height=28)
        right_button.noBackgroundColor()
        right_button.writeLine("➡️")
        right_button.enableFeedback("f", lambda *args: self.moveShapeRight())

        AutoPin('V',
                AutoPin('S'),
                AutoPin('H', left_button, right_button)).pin(self.dd)

        self.score = score
        self.pen = pen

        self.shape = Shape()
        #self.drawGrid()

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

        if not self.shape.move_down():
            won = self.checkGrid()
            if won:
                self.shape = None
                print("*** YOU WON ***")
            else:
                if self.shape.block.y > 0:
                    self.shape.reset()
                else:
                    self.shape = None
                    print("*** GAME OVER ***")

        if self.shape is not None:
            self.drawGrid()

    def drawGrid(self):
        self.dd.freezeDrawing()
        draw_grid(shape=self.shape, pen=self.pen)
        self.dd.unfreezeDrawing()


    def checkGrid(self) -> bool:
        return check_grid(shape=self.shape, score=self.score)

    def moveShapeLeft(self):
        if self.shape.move_left():
            self.drawGrid()

    def moveShapeRight(self):
        if self.shape.move_right():
            self.drawGrid()


if __name__ == "__main__":
    from dumbdisplay_examples.utils import create_example_wifi_dd, DDAppBase
    app = TetrisOneBlockApp(create_example_wifi_dd())
    app.run()
