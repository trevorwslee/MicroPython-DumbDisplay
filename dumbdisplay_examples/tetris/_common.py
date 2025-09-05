import random

from dumbdisplay.layer_turtle import LayerTurtle




_width = 400
_height = 700
_top = 230
_left = -110
_block_unit_width = 20
#_colors = ['black', 'red', 'lightblue', 'blue', 'orange', 'yellow', 'green', 'purple']
_colors = ['black', 'crimson', 'cyan', 'ivory', 'coral', 'gold', 'lime', 'magenta']

_grid_n_cols = 12
_grid_n_rows = 24


class Grid:
    def __init__(self, grid_cells):
        self.grid_cells = grid_cells
        self.grid_dirty = []
        for grid_row in self.grid_cells:
            grid_dirty_row = []
            for cell in grid_row:
                dirty = True if cell != 0 else False
                grid_dirty_row.append(dirty)
            self.grid_dirty.append(grid_dirty_row)
        self.n_cols = len(self.grid_cells[0])
        self.n_rows = len(self.grid_cells)

    def check_reset_need_redraw(self, row_idx, col_idx):
        dirty = self.grid_dirty[row_idx][col_idx]
        if not dirty:
            return False
        self.grid_dirty[row_idx][col_idx] = False
        return True

    def get_value(self, row_idx, col_idx):
        return self.grid_cells[row_idx][col_idx]

    def set_value(self, row_idx, col_idx, value):
        if self.grid_cells[row_idx][col_idx] != value:
            self.grid_cells[row_idx][col_idx] = value
            self.grid_dirty[row_idx][col_idx] = True


class Block:
    def __init__(self, x: int, y: int, block_grid: Grid, block_pen: LayerTurtle, rotate_with_level: bool = False):
        self.x = x
        self.y = y
        self.rotation = 0
        self.block_grid = block_grid
        self.block_pen = block_pen
        self.rotate_with_level = rotate_with_level
        self.move_reach_in_millis = 50
        block_pen.clear()
        if not rotate_with_level:
            # make the block tiled a bit
            block_pen.setLevelRotation(2, 90, 120)  # calculated from _left and _top
        self.sync_image()
        _draw_grid(block_grid, block_pen)

    def move_down(self, grid: Grid) -> bool:
        if _check_bad_block_grid_placement(self.block_grid, self.x, self.y + 1, grid=grid):
            return False
        self.y += 1
        self.sync_image(self.move_reach_in_millis)
        return True

    def move_right(self, grid: Grid) -> bool:
        if _check_bad_block_grid_placement(self.block_grid, self.x + 1, self.y, grid=grid):
            return False
        self.x += 1
        self.sync_image(self.move_reach_in_millis)
        return True

    def move_left(self, grid: Grid) -> bool:
        if _check_bad_block_grid_placement(self.block_grid, self.x - 1, self.y, grid=grid):
            return False
        self.x -= 1
        self.sync_image(self.move_reach_in_millis)
        return True

    def rotate(self, grid: Grid) -> bool:
        (rotated_block_grid, y_offset) = _rotate_block_grid_if_possible(self.block_grid, self.x, self.y, grid=grid)
        if rotated_block_grid is None:
            return False
        self.block_grid = rotated_block_grid
        self.y += y_offset
        self.rotation = (self.rotation + 90) % 360
        if self.rotate_with_level:
            self.sync_image(self.move_reach_in_millis)
        else:
            self.block_pen.clear()
            _draw_grid(self.block_grid, self.block_pen)
        return True


    def sync_image(self, reach_in_millis: int = 0):
        anchor_x = self.x * _block_unit_width
        anchor_y = self.y * _block_unit_width
        self.block_pen.setLevelAnchor(anchor_x, anchor_y, reach_in_millis)
        if self.rotate_with_level:
            self.block_pen.setLevelRotation(self.rotation + 2, 90 + 10, 120 + 10, reach_in_millis)  # calculated from _left and _top



def _check_bad_block_grid_cells_placement(grid_cells: list[list[int]], block_grid_x_off: int, block_grid_y_offset: int, grid: Grid, check_boundary: bool = True) -> bool:
    n_rows = len(grid_cells)
    n_cols = len(grid_cells[0]) if n_rows > 0 else 0
    for y in range(n_rows):
        for x in range(n_cols):
            if grid_cells[y][x] != 0:
                row_idx = y + block_grid_y_offset
                col_idx = x + block_grid_x_off
                if row_idx < 0:
                    continue  # never mind above the grid
                if row_idx < 0 or row_idx >= grid.n_rows:
                    if not check_boundary:
                        continue
                    return True
                if col_idx < 0 or col_idx >= grid.n_cols:
                    if not check_boundary:
                        continue
                    return True
                if grid.get_value(row_idx, col_idx) != 0:
                    return True
    return False


def _rotate_block_grid_cells(grid_cells: list[list[int]]) -> list[list[int]]:
    rotated = []
    for x in range(len(grid_cells[0])):
        new_row = []
        for y in range(len(grid_cells) -1, -1, -1):
            new_row.append(grid_cells[y][x])
        rotated.append(new_row)
    return rotated


def _randomize_grid(randomize_row_count: int) -> Grid:
    grid_cells = []
    for y in range(_grid_n_rows):
        grid_row = []
        for x in range(_grid_n_cols):
            if y >= (_grid_n_rows - randomize_row_count) and random.random() < 0.7:
                color = random.randint(1, len(_colors) - 1)
            else:
                color = 0
            grid_row.append(color)
        grid_cells.append(grid_row)
    return Grid(grid_cells=grid_cells)


def _draw(x, y, color_number, pen: LayerTurtle):
    screen_x = _left + (x * _block_unit_width) # each turtle 20x20 pixels
    screen_y = _top - (y * _block_unit_width)
    # (screen_x, screen_y) = _calc_screen_position(x, y)
    color = _colors[color_number]
    pen.penColor(color)
    pen.goTo(screen_x, screen_y, with_pen=False)
    pen.rectangle(_block_unit_width - 2, _block_unit_width - 2, centered=True)

# def _draw_block(block: 'Block', block_pen: LayerTurtle):
#     block_pen.clear()
#     _draw(block.x, block.y, block.color, block_pen)

def _draw_grid(grid: Grid, pen: LayerTurtle):
    for y in range(grid.n_rows):
        for x in range(grid.n_cols):
            if not grid.check_reset_need_redraw(y, x):
                continue
            color_number = grid.get_value(y, x)
            _draw(x, y, color_number, pen)

def _check_bad_block_grid_placement(block_grid: Grid, block_grid_x_off: int, block_grid_y_offset: int, grid: Grid, check_boundary: bool = True) -> bool:
    if True:
        return _check_bad_block_grid_cells_placement(block_grid.grid_cells, block_grid_x_off, block_grid_y_offset, grid, check_boundary)
    else:
        for y in range(block_grid.n_rows):
            for x in range(block_grid.n_cols):
                if block_grid.get_value(y, x) != 0:
                    row_idx = y + block_grid_y_offset
                    col_idx = x + block_grid_x_off
                    if row_idx < 0:
                        continue  # never mind above the grid
                    if row_idx < 0 or row_idx >= grid.n_rows:
                        if not check_boundary:
                            continue
                        return True
                    if col_idx < 0 or col_idx >= grid.n_cols:
                        if not check_boundary:
                            continue
                        return True
                    if grid.get_value(row_idx, col_idx) != 0:
                        return True
        return False


def _rotate_block_grid_if_possible(block_grid: Grid, block_grid_x_off: int, block_grid_y_offset: int, grid: Grid) -> (Grid, int):
    block_grid_cells = block_grid.grid_cells
    rotated_cells = _rotate_block_grid_cells(block_grid_cells)
    y_offset = len(rotated_cells) - len(block_grid_cells)
    if _check_bad_block_grid_cells_placement(rotated_cells, block_grid_x_off, block_grid_y_offset + y_offset, grid, check_boundary=True):
        return (None, None)
    rotated_block_grid = Grid(grid_cells=rotated_cells)
    return (rotated_block_grid, y_offset)


def _commit_block_grid(block_grid: Grid, block_grid_x_off: int, block_grid_y_offset: int, grid: Grid):
    for y in range(block_grid.n_rows):
        for x in range(block_grid.n_cols):
            color = block_grid.get_value(y, x)
            if color != 0:
                grid.set_value(y + block_grid_y_offset, x + block_grid_x_off, color)

