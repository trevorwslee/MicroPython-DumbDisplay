from dumbdisplay.core import *
from dumbdisplay.layer_graphical import DDRootLayer
from dumbdisplay.layer_turtle import LayerTurtle


_WIDTH = 400
_HEIGHT = 700
_PEN_FILED = True


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




class _Shape():
    def __init__(self, grid):
        self.x = 5
        self.y = 0
        self.color = 4
        self.grid = grid
        self.move = 'go'

    def move_right(self):
        if self.x < 11 and self.move == 'go':
            if _grid[self.y][self.x + 1]==0:
                _grid[self.y][self.x]=0
                self.x += 1
                _grid[self.y][self.x] = self.color

    def move_left(self):
        if self.x > 0 and self.move == 'go':
            if _grid[self.y][self.x - 1]==0:
                _grid[self.y][self.x]=0
                self.x -= 1
                _grid[self.y][self.x] = self.color


class TetrisOneBlockApp():
    def __init__(self, dd: DumbDisplay):
        self.dd = dd
        self.root: DDRootLayer = None
        self.score: LayerTurtle = None
        self.pen: LayerTurtle = None
        self.score_count = 0

    def run(self):
        while True:
            (connected, reconnecting) = self.dd.connectPassive()
            if connected:
                if self.root is None:
                    self.initializeDD()
                elif reconnecting:
                    self.dd.masterReset()
                    self.root = None
                else:
                    self.updateDD()

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
        if _PEN_FILED:
            pen.penFilled()
        #pen.up()
        # pen.speed(0)
        # pen.shape('square')
        # pen.shapesize(0.9, 0.9)
        # pen.setundobuffer(None)

        self.root = root
        self.score = score
        self.pen = pen

        shape = _Shape(_grid)
        _grid[shape.y][shape.x] = shape.color

        self.draw_grid(_grid)

    def updateDD(self):
        pass

    def draw_grid(self, grid):
        self.dd.freezeDrawing()
        self.pen.clear()
        top = 230
        left = -110
        colors = ['black', 'red', 'lightblue', 'blue', 'orange', 'yellow', 'green',
                  'purple']

        for y in range(len(grid)): # 24 rows
            for x in range(len(grid[0])): # 12 columns
                screen_x = left + (x*20) # each turtle 20x20 pixels
                screen_y = top - (y*20)
                color_number = grid[y][x]
                if color_number == 0:
                    continue
                color = colors[color_number]
                self.pen.penColor(color)
                self.pen.goTo(screen_x, screen_y, with_pen=False)
                #self.pen.stamp()
                if _PEN_FILED:
                    self.pen.rectangle(18, 18, centered=True)
                else:    # TODO: thing of a faster way
                    self.pen.fillColor(color)
                    self.pen.beginFill()
                    self.pen.rectangle(18, 18, centered=True)
                    self.pen.endFill()
        self.dd.unfreezeDrawing()


    def check_grid(self):
        #global score_count
        # Check if each row is full:
        for y in range(0,24):
            is_full = True
            y_erase = y
            for x in range(0,12):
                if _grid[y][x] == 0:
                    is_full = False
                    break
            # Remove row and shift down
            if is_full:
                self.score_count += 1
                self.score.clear()
                self.score.write(f'Score: {self.score_count}', align='center')

                for y in range(y_erase-1, -1, -1):
                    for x in range(0,12):
                        _grid[y+1][x] = _grid[y][x]


if __name__ == "__main__":
    from dumbdisplay_examples.utils import create_example_wifi_dd
    app = TetrisOneBlockApp(create_example_wifi_dd())
    app.run()
