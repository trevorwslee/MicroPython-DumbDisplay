# ***
# *** Adapted from TETRIS CLASSIC\tetris_turtle.py of https://github.com/DimaGutierrez/Python-Games
# *** - modified from dumbdisplay_examples/tetris_classic
# ***
import random
import time

from dumbdisplay.core import *
from dumbdisplay.layer_graphical import DDRootLayer
from dumbdisplay.layer_turtle import LayerTurtle
from dumbdisplay.layer_lcd import LayerLcd

from dumbdisplay_examples.utils import DDAppBase, create_example_wifi_dd


_DRAW_SHAP_AFTER_MOVE = True

_delay = 0.5

_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

_grid_dirty = None
#_dirty = False

class GridRow():
    def __len__(self):
        return len(_grid[self.row_idx])
    def __getitem__(self, col_idx):
        return _grid[self.row_idx][col_idx]
    def __setitem__(self, col_idx, value):
        #global _dirty
        _grid[self.row_idx][col_idx] = value
        _grid_dirty[self.row_idx][col_idx] = True
        #_dirty = True

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
        self.grid_row = GridRow()
    def __len__(self):
        return len(_grid)
    def __getitem__(self, row_idx):
        self.grid_row.row_idx = row_idx
        return self.grid_row
    def check_reset_need_redraw(self, row_idx, col_idx):
        dirty = _grid_dirty[row_idx][col_idx]
        if not dirty:
            return False
        _grid_dirty[row_idx][col_idx] = False
        return True


grid = Grid()
score_count = 0

class Shape():
    def __init__(self):
        self.x = 5
        self.y = 0
        self.color = random.randint(1, 7)

        # Block Shape
        square = [[1,1],
                  [1,1]]

        horizontal_line = [[1,1,1,1]]

        vertical_line = [[1],
                         [1],
                         [1],
                         [1]]

        left_l = [[1,0,0,0],
                  [1,1,1,1]]

        right_l = [[0,0,0,1],
                   [1,1,1,1]]

        left_s = [[1,1,0],
                  [0,1,1]]

        right_s = [[0,1,1],
                   [1,1,0]]

        t = [[0,1,0],
             [1,1,1]]

        shapes = [square, horizontal_line, vertical_line, left_l, right_l, left_s, right_s, t]

        # Choose a random shape each time
        self.shape = random.choice(shapes)


        self.height = len(self.shape)
        self.width = len(self.shape[0])

        # print(self.height, self.width)

    def move_left(self):
        if self.x > 0:
            if grid[self.y][self.x - 1] == 0:
                self.erase_shape()
                self.x -= 1
                if _DRAW_SHAP_AFTER_MOVE:
                    self.draw_shape()

    def move_right(self):
        if self.x < 12 - self.width:
            if grid[self.y][self.x + self.width] == 0:
                self.erase_shape()
                self.x += 1
                if _DRAW_SHAP_AFTER_MOVE:
                    self.draw_shape()

    def draw_shape(self):
        for y in range(self.height):
            for x in range(self.width):
                if(self.shape[y][x]==1):
                    grid[self.y + y][self.x + x] = self.color

    def erase_shape(self):
        for y in range(self.height):
            for x in range(self.width):
                if(self.shape[y][x]==1):
                    grid[self.y + y][self.x + x] = 0

    def can_move(self):
        result = True
        for x in range(self.width):
            # Check if bottom is a 1
            if(self.shape[self.height-1][x] == 1):
                if(grid[self.y + self.height][self.x + x] != 0):
                    result = False
        return result

    def rotate(self):
        # First erase_shape
        self.erase_shape()
        rotated_shape = []
        for x in range(len(self.shape[0])):
            new_row = []
            for y in range(len(self.shape)-1, -1, -1):
                new_row.append(self.shape[y][x])
            rotated_shape.append(new_row)

        right_side = self.x + len(rotated_shape[0])
        if right_side < len(grid[0]):
            self.shape = rotated_shape
            # Update the height and width
            self.height = len(self.shape)
            self.width = len(self.shape[0])

def draw_grid(pen: LayerTurtle):
    #pen.clear()
    top = 230
    left = -110

    colors = ["black", "lightblue", "blue", "orange", "yellow", "green", "purple", "red"]

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if not grid.check_reset_need_redraw(y, x):
                continue
            screen_x = left + (x * 20)
            screen_y = top - (y * 20)
            color_number = grid[y][x]
            color = colors[color_number]
            pen.penColor(color)
            pen.goTo(screen_x, screen_y, with_pen=False)
            #pen.stamp()
            pen.rectangle(18, 18, centered=True)


def check_grid(score: LayerTurtle):
    # Check if each row is full
    y = 23
    while y > 0:
        is_full = True
        for x in range(0, 12):
            if grid[y][x] == 0:
                is_full = False
                y -= 1
                break
        if is_full:
            global score_count
            score_count += 10
            score.clear()
            score.write(f'Score: {score_count}', align='C')

            for copy_y in range(y, 0, -1):
                for copy_x in range(0, 12):
                    grid[copy_y][copy_x] = grid[copy_y-1][copy_x]

# def draw_score(pen: LayerTurtle):
#     pen.penColor("blue")
#     #pen.hideturtle()
#     pen.goTo(-75, 350, with_pen=False)
#     #pen.write("Score: {}".format(score), move=False, align="left", font=("Arial", 24, "normal"))
#     pen.write("Score: {}".format(score), align="L")



class TetrisClassicApp(DDAppBase):
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
        border.write("TETRIS", "C")

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

        self.root = root
        self.score = score
        self.pen = pen
        self.left_button = left_button
        self.right_button = right_button

        # Create the basic shape for the start of the game
        shape = Shape()

        # # Put the shape in the grid
        # grid[shape.y][shape.x] = shape.color

        self.shape = shape

        # wn.listen()
        # wn.onkeypress(lambda: shape.move_left(grid), "a")
        # wn.onkeypress(lambda: shape.move_right(grid), "d")
        # wn.onkeypress(lambda: shape.rotate(grid), "space")

    def updateDD(self):
        #global _dirty
        now = time.time()
        need_update = self.last_update_time is None or (now - self.last_update_time) >= _delay
        if need_update:
            self.update()
            self.last_update_time = now
            #_dirty = False
        # else:
        #     if _dirty:
        #         self.drawGrid()
        #         _dirty = False

    def update(self):
        # Move the shape
        # Open Row
        # Check for the bottom
        if self.shape.y == 23 - self.shape.height + 1:
            self.shape = Shape()
            self.checkGrid()
        # Check for collision with next row
        elif self.shape.can_move():
            # Erase the current shape
            self.shape.erase_shape()

            # Move the shape by 1
            self.shape.y +=1

            # Draw the shape again
            self.shape.draw_shape()

        else:
            self.shape = Shape()
            self.checkGrid()

        # Draw the screen
        self.drawGrid()
        #draw_score(pen, score)

    def drawGrid(self):
        self.dd.freezeDrawing()
        draw_grid(pen=self.pen)
        self.dd.unfreezeDrawing()

    def checkGrid(self):
        check_grid(score=self.score)

    def moveShapeLeft(self):
        self.shape.move_left()
        self.drawGrid()

    def moveShapeRight(self):
        self.shape.move_right()
        self.drawGrid()


if __name__ == "__main__":
    from dumbdisplay_examples.utils import create_example_wifi_dd, DDAppBase
    app = TetrisClassicApp(create_example_wifi_dd())
    app.run()
