import random

from dumbdisplay_examples.tetris._common import Grid, _colors

_square = [[1,1],
           [1,1]]

_horizontal_line = [[1,1,1,1]]

_vertical_line = [[1],
                  [1],
                  [1],
                  [1]]

_left_l = [[1,0,0,0],
           [1,1,1,1]]

_right_l = [[0,0,0,1],
            [1,1,1,1]]

_left_s = [[1,1,0],
           [0,1,1]]

_right_s = [[0,1,1],
            [1,1,0]]

_t = [[0,1,0],
      [1,1,1]]

_shapes = [_square, _horizontal_line, _vertical_line, _left_l, _right_l, _left_s, _right_s, _t]


def _randomize_block_grid() -> Grid:
    block_grid = random.choice(_shapes)
    # if True:
    #     block_grid = _t
    color = random.randint(1, len(_colors) - 1)
    block_grid_cell_type = block_grid
    block_grid = [[color if cell != 0 else 0 for cell in row] for row in block_grid]
    return Grid(grid_cells=block_grid, grid_cell_type=block_grid_cell_type)

