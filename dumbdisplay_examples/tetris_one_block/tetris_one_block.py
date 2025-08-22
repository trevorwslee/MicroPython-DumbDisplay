import time

from dumbdisplay.core import *
from dumbdisplay.layer_graphical import DDRootLayer
from dumbdisplay.layer_turtle import LayerTurtle
from dumbdisplay.layer_lcd import LayerLcd

from dumbdisplay_examples.utils import DDAppBase, create_example_wifi_dd

_WIDTH = 400
_HEIGHT = 700


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

_grid_dirty = None

class GridRow():
    def __init__(self, row_idx):
        self.row_idx = row_idx
    def __len__(self):
        return len(_grid[self.row_idx])
    def __getitem__(self, col_idx):
        return _grid[self.row_idx][col_idx]
    def __setitem__(self, col_idx, value):
        _grid[self.row_idx][col_idx] = value
        _grid_dirty[self.row_idx][col_idx] = True

class Grid():
    def __init__(self):
        global _grid_dirty
        if _grid_dirty is None:
            _grid_dirty = []
            for grid_row in _grid:
                grid_dirty_row = []
                for cell in grid_row:
                    dirty = True if cell != 0 else False
                    grid_dirty_row.append(dirty)
                _grid_dirty.append(grid_dirty_row)

    def __len__(self):
        return len(_grid)
    def __getitem__(self, row_idx):
        return GridRow(row_idx)
    def is_dirty(self, row_idx, col_idx):
        return _grid_dirty[row_idx][col_idx] != 0
        #return _grid_dirty[row_idx][col_idx]

grid = Grid()
score_count = 0


class Shape():
    def __init__(self):
        self.x = 5
        self.y = 0
        self.color = 4
        self.move = 'go'

    def move_right(self):
        if self.x < 11 and self.move == 'go':
            if grid[self.y][self.x + 1]==0:
                grid[self.y][self.x]=0
                self.x += 1
                grid[self.y][self.x] = self.color

    def move_left(self):
        if self.x > 0 and self.move == 'go':
            if grid[self.y][self.x - 1]==0:
                grid[self.y][self.x]=0
                self.x -= 1
                grid[self.y][self.x] = self.color


def _draw_grid(pen: LayerTurtle):
    pen.clear()
    top = 230
    left = -110
    colors = ['black', 'red', 'lightblue', 'blue', 'orange', 'yellow', 'green',
              'purple']

    for y in range(len(grid)): # 24 rows
        for x in range(len(grid[0])): # 12 columns
            screen_x = left + (x*20) # each turtle 20x20 pixels
            screen_y = top - (y*20)
            if not grid.is_dirty(y, x):
                continue
            color_number = grid[y][x]
            color = colors[color_number]
            pen.penColor(color)
            pen.goTo(screen_x, screen_y, with_pen=False)
            #self.pen.stamp()
            pen.rectangle(18, 18, centered=True)


def _check_grid(score: LayerTurtle):
    global score_count
    # Check if each row is full:
    for y in range(0,24):
        is_full = True
        y_erase = y
        for x in range(0,12):
            if grid[y][x] == 0:
                is_full = False
                break
        # Remove row and shift down
        if is_full:
            score_count += 1
            score.clear()
            score.write(f'Score: {score_count}', align='center')

            for y in range(y_erase-1, -1, -1):
                for x in range(0,12):
                    grid[y + 1][x] = grid[y][x]



class TetrisOneBlockApp(DDAppBase):
    def __init__(self, dd: DumbDisplay = create_example_wifi_dd()):
        super().__init__(dd)
        self.root: DDRootLayer = None
        self.score: LayerTurtle = None
        self.pen: LayerTurtle = None
        self.left_button: LayerLcd = None
        self.right_button: LayerLcd = None
        self.shape: Shape = None
        self.last_update_time = None

    def initializeDD(self):

        root = DDRootLayer(self.dd, _WIDTH, _HEIGHT)
        root.border(5, "darkred", "round", 1)
        root.backgroundColor("black")

        score = LayerTurtle(self.dd, _WIDTH, _HEIGHT)
        score.penColor('red')
        score.penUp()
        #score.hideturtle()
        score.goTo(60, -300)
        #score.write('Score: 0', align='center', font=('Courier', 24, 'normal'))
        score.setTextFont("Courier", 24)
        score.write('Score: 0', 'C')

        border = LayerTurtle(self.dd, _WIDTH, _HEIGHT)
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
        border.write("TETRIS", "C")

        pen = LayerTurtle(self.dd, _WIDTH, _HEIGHT)
        #pen.up()
        # pen.speed(0)
        # pen.shape('square')
        # pen.shapesize(0.9, 0.9)
        # pen.setundobuffer(None)
        pen.penFilled()


        left_button = LayerLcd(self.dd, 2, 1, char_height=28)
        left_button.noBackgroundColor()
        left_button.writeLine("⬅️")

        right_button = LayerLcd(self.dd, 2, 1, char_height=28)
        right_button.noBackgroundColor()
        right_button.writeLine("➡️")

        AutoPin('V',
                AutoPin('S'),
                AutoPin('H', left_button, right_button)).pin(self.dd)


        self.root = root
        self.score = score
        self.pen = pen
        self.left_button = left_button
        self.right_button = right_button

        shape = Shape()
        grid[shape.y][shape.x] = shape.color

        self.shape = shape

        self.drawGrid()

    def updateDD(self):
        now = time.time()
        need_update = self.last_update_time is None or (now - self.last_update_time) > 0.2
        if need_update:
            self.update()
            self.last_update_time = now

    def update(self):
        # Move shape
        # Stop if at the bottom
        if self.shape.y == 23:
            self.shape.move = 'stop'
            self.checkGrid()
            self.shape = Shape()

        # Drop down one space if empty below
        elif grid[self.shape.y + 1][self.shape.x] == 0:
            grid[self.shape.y][self.shape.x]=0
            self.shape.y += 1
            grid[self.shape.y][self.shape.x] = self.shape.color

        # Stop if above another block
        else:
            self.shape.move = 'stop'
            self.shape = Shape()
            self.checkGrid()

        # Had to place it here for upcoming shapes...
        # win.onkey(shape.move_right, 'Right')
        # win.onkey(shape.move_left, 'Left')


        self.drawGrid()
        #time.sleep(0.1)

    def drawGrid(self):
        self.dd.freezeDrawing()
        _draw_grid(pen=self.pen)
        self.dd.unfreezeDrawing()


    def checkGrid(self):
        _check_grid(score=self.score)


if __name__ == "__main__":
    from dumbdisplay_examples.utils import create_example_wifi_dd, DDAppBase

    app = TetrisOneBlockApp(create_example_wifi_dd())
    app.run()
