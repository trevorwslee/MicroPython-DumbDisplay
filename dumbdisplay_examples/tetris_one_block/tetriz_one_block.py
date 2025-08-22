from dumbdisplay.core import *
from dumbdisplay.layer_graphical import DDRootLayer
from dumbdisplay.layer_turtle import LayerTurtleTracked


_WIDTH = 400
_HEIGHT = 700


class Shape():
    def __init__(self, grid):
        self.x = 5
        self.y = 0
        self.color = 4
        self.grid = grid
        self.move = 'go'

    def move_right(self):
        if self.x < 11 and self.move == 'go':
            if grid[self.y][self.x+1]==0:
                grid[self.y][self.x]=0
                self.x += 1
                grid[self.y][self.x] = self.color

    def move_left(self):
        if self.x > 0 and self.move == 'go':
            if grid[self.y][self.x-1]==0:
                grid[self.y][self.x]=0
                self.x -= 1
                grid[self.y][self.x] = self.color


grid = [
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


class TetrisOneBlockApp():
    def __init__(self, dd: DumbDisplay):
        self.dd = dd
        self.root = None
        self.score = None

    def run(self):
        while True:
            (connected, reconnecting) = self.dd.connectPassive()
            if connected:
                if self.root is None:
                    self.initializeDD()
                elif reconnecting:
                    self.dd.masterReset()
                    self.board = None
                else:
                    self.updateDD()
            elif reconnecting:
                self.dd.masterReset()
                self.root = None

    def initializeDD(self):

        root = DDRootLayer(self.dd, _WIDTH, _HEIGHT)
        root.border(5, "darkred", "round", 1)
        root.backgroundColor("black")

        score = LayerTurtleTracked(self.dd, _WIDTH, _HEIGHT)
        score.penColor('red')
        score.penUp()
        #score.hideturtle()
        score.goTo(60, -300)
        #score.write('Score: 0', align='center', font=('Courier', 24, 'normal'))
        score.setTextFont("Courier", 24)
        score.write('Score: 0', 'C')

        border = LayerTurtleTracked(self.dd, _WIDTH, _HEIGHT)
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


        self.root = root
        self.score = score

    def updateDD(self):
        pass


if __name__ == "__main__":
    from dumbdisplay_examples.utils import create_example_wifi_dd
    app = TetrisOneBlockApp(create_example_wifi_dd())
    app.run()
