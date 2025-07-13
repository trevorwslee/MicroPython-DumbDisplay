import random


class BoardManager:
    def __init__(self, tile_count: int):
        self.tile_count = tile_count
        self.board_tiles = [i for i in range(tile_count * tile_count)]
        self.hole_tile_col_idx = 0
        self.hole_tile_row_idx = 0
        self.randomize_can_move_from_dirs = [0, 0, 0, 0]
        self.randomize_can_move_from_dir = -1
    def clone(self):
        new_board_manager = BoardManager(self.tile_count)
        new_board_manager.board_tiles = self.board_tiles.copy()
        new_board_manager.hole_tile_col_idx = self.hole_tile_col_idx
        new_board_manager.hole_tile_row_idx = self.hole_tile_row_idx
        new_board_manager.randomize_can_move_from_dirs = self.randomize_can_move_from_dirs.copy()
        new_board_manager.randomize_can_move_from_dir = self.randomize_can_move_from_dir
        return new_board_manager
    def showBoard(self):
        for col_idx in range(self.tile_count):
            for row_idx in range(self.tile_count):
                #tile_idx = col_idx * self.tile_count + row_idx
                tile_id = self.board_tiles[col_idx * self.tile_count + row_idx]
                if row_idx == 0:
                    if col_idx == 0:
                        print(self.tile_count * "-----" + "-")
                    print("|", end="")
                print(f" {tile_id:2} |", end="")
                if row_idx == (self.tile_count - 1):
                    print()
                    if col_idx == (self.tile_count - 1):
                        print(self.tile_count * "-----" + "-")
            #print()
    def randomizeBoardStepGetMove(self) -> int:
        self.randomizeBoardStep()
        move = self.randomize_can_move_from_dir
        if move == 0:
            move = 1
        elif move == 2:
            move = 3
        elif move == 3:
            move = 2
        else:
            move = 0
        return move
    def randomizeBoardStep(self) -> tuple[int, int, int]:
        can_count = self.checkCanMoveFromDirs(self.randomize_can_move_from_dir)
        self.randomize_can_move_from_dir = self.randomize_can_move_from_dirs[random.randint(0, can_count - 1)]
        (from_col_idx, from_row_idx) = self.canMoveFromDirToFromIdxes(self.randomize_can_move_from_dir)
        to_col_idx = self.hole_tile_col_idx
        to_row_idx = self.hole_tile_row_idx
        from_tile_id = self.board_tiles[from_row_idx * self.tile_count + from_col_idx]
        self.board_tiles[from_row_idx * self.tile_count + from_col_idx] = self.board_tiles[self.hole_tile_row_idx * self.tile_count + self.hole_tile_col_idx]
        self.board_tiles[self.hole_tile_row_idx * self.tile_count + self.hole_tile_col_idx] = from_tile_id
        self.hole_tile_col_idx = from_col_idx
        self.hole_tile_row_idx = from_row_idx
        return (to_col_idx, to_row_idx, from_tile_id)
    def moveTileFromDir(self, from_dir: int) -> int:
        (from_col_idx, from_row_idx) = self.canMoveFromDirToFromIdxes(from_dir)
        return self.moveTileFromIdxes(from_col_idx, from_row_idx)
    def moveTileFromIdxes(self, from_col_idx: int, from_row_idx: int) -> int:
        prev_hole_tile_id = self.board_tiles[self.hole_tile_row_idx * self.tile_count + self.hole_tile_col_idx]
        self.board_tiles[self.hole_tile_row_idx * self.tile_count + self.hole_tile_col_idx] = self.board_tiles[from_row_idx * self.tile_count + from_col_idx]
        self.board_tiles[from_row_idx * self.tile_count + from_col_idx] = prev_hole_tile_id
        self.hole_tile_col_idx = from_col_idx
        self.hole_tile_row_idx = from_row_idx
        return prev_hole_tile_id
    def checkBoardSolved(self) -> bool:
        for row_tile_idx in range(0, self.tile_count):
            for col_tile_idx in range(0, self.tile_count):
                tile_id = col_tile_idx + row_tile_idx * self.tile_count
                board_tile_id = self.board_tiles[row_tile_idx * self.tile_count + col_tile_idx]
                if board_tile_id != tile_id:
                    return False
        return True
    def checkCanMoveFromDirs(self, prev_can_move_from_dir: int) -> int:
        can_count = 0
        if self.hole_tile_col_idx > 0 and prev_can_move_from_dir != 1:
            self.randomize_can_move_from_dirs[can_count] = 0;  # 0: left
            can_count += 1
        if self.hole_tile_col_idx < (self.tile_count - 1) and prev_can_move_from_dir != 0:
            self.randomize_can_move_from_dirs[can_count] = 1  # 1: right
            can_count += 1
        if self.hole_tile_row_idx > 0 and prev_can_move_from_dir != 3:
            self.randomize_can_move_from_dirs[can_count] = 2  # 2: up
            can_count += 1
        if self.hole_tile_row_idx < (self.tile_count - 1) and prev_can_move_from_dir != 2:
            self.randomize_can_move_from_dirs[can_count] = 3  # 3: down
            can_count += 1
        return can_count
    def canMoveFromDirToFromIdxes(self, can_move_from_dir: int):
        if can_move_from_dir == 0:
            from_col_idx = self.hole_tile_col_idx - 1
            from_row_idx = self.hole_tile_row_idx
        elif can_move_from_dir == 1:
            from_col_idx = self.hole_tile_col_idx + 1
            from_row_idx = self.hole_tile_row_idx
        elif can_move_from_dir == 2:
            from_col_idx = self.hole_tile_col_idx
            from_row_idx = self.hole_tile_row_idx - 1
        else:
            from_col_idx = self.hole_tile_col_idx
            from_row_idx = self.hole_tile_row_idx + 1
        return (from_col_idx, from_row_idx)
