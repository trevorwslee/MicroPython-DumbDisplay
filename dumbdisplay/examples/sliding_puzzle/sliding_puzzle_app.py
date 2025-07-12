import random
import time
from dumbdisplay.core import *
from dumbdisplay.examples.sliding_puzzle.board_manager import BoardManager
from dumbdisplay.layer_graphical import LayerGraphical

BOARD_SIZE = 400
DEF_TILE_COUNT = 4  # the default sliding puzzle is 4x4; i.e. 16 tiles


class SlidingPuzzleApp:
    def __init__(self, dd: DumbDisplay, tile_count: int = DEF_TILE_COUNT):
        self.tile_count = tile_count
        self.tile_size = BOARD_SIZE / tile_count
        self.dd = dd
        self.board: LayerGraphical = None
        #self.board_initialized = False

        self.board_manager: BoardManager = None
        #self.board_tiles = [i for i in range(self.tile_count * self.tile_count)]
        #self.hole_tile_col_idx = -1  # -1 means board not initialize
        #self.hole_tile_row_idx = -1
        #self.randomize_can_move_from_dirs = [-1, -1, -1, -1]
        #self.randomize_can_move_from_dir = -1

        self.randomize_move_tile_in_millis = 0
        self.waiting_to_restart_millis = -1  # -1 means not waiting
        self.init_randomize_tile_step_count = 0
        self.randomize_tiles_step_count = 0
        self.move_tile_col_idx = -1
        self.move_tile_row_idx = -1
        self.move_tile_from_dir = -1
        self.move_tile_delta = -1
        self.move_tile_ref_x = -1
        self.move_tile_ref_y = -1
        self.move_tile_id = -1


    def run(self):
        while True:
            (connected, reconnecting) = self.dd.connectPassive()
            if connected:
                if self.board is None:
                    self.initializeDD()
                elif reconnecting:
                    self.dd.masterReset()
                    self.board = None
                else:
                    self.updateDD()
            elif reconnecting:
                self.dd.masterReset()
                self.board = None


    def initializeDD(self):
        board = LayerGraphical(self.dd, BOARD_SIZE, BOARD_SIZE)
        board.backgroundColor("teal")
        board.border(8, "navy", "round", 5)
        board.drawRect(0, 0, BOARD_SIZE, BOARD_SIZE, "azure", True)
        board.drawRoundRect(20, 20, BOARD_SIZE - 40, BOARD_SIZE - 40, 10, "aqua", True)

        board.drawImageFileFit("dumbdisplay.png")
        board.setTextFont("DL::Roboto");
        board.drawTextLine("In God We Trust", 34, "C", "white", "purple", 32)          # C is for centering on the line (from left to right)
        board.drawTextLine("❤️ May God bless you ❤️", 340, "R-20", "purple", "", 20)   # R is for right-justify align on the line; with -20 offset from right

        board.enableFeedback()

        self.board = board

        self.board_manager = None
        # self.board_initialized = False
        # self.hole_tile_col_idx = -1
        # self.hole_tile_row_idx = -1
        self.randomize_tiles_step_count = 0
        self.waiting_to_restart_millis = 0


    def updateDD(self):
        if self.waiting_to_restart_millis != -1:
            # starts off waiting for double tab
            now_millis = time.ticks_ms()
            diff_millis = now_millis - self.waiting_to_restart_millis
            if diff_millis > 15000:
                self.dd.log("! double tab to start !")
                self.waiting_to_restart_millis = now_millis

        board_feedback = self.board.getFeedback()  # ensure the board feedback is updated
        if self.randomize_tiles_step_count > 0:
            # randomizing the board
            self.randomizeTilesStep()
            self.randomize_tiles_step_count -= 1
            if self.randomize_tiles_step_count == 0:
                # randomization is done
                self.dd.log("... done randomizing board")
                self.board.enableFeedback(":drag")  # :drag to allow dragging that produces MOVE feedback type (and ended with -1, -1 MOVE feedbackv)
        else:
            if board_feedback is not None:
                if board_feedback.type == "doubleclick":
                    # double click ==> randomize the board, even during play
                    self.board.flash()
                    self.board.disableFeedback()
                    self.ensureBoardInitialized()
                    self.dd.log("Randomizing board ...")
                    self.waiting_to_restart_millis = -1
                    self.startRandomizeBoard()
                    return
                elif board_feedback.type == "move":
                    # dragging / moving a tile ... handle it in onBoardDragged
                    if self.onBoardDragged(board_feedback.x, board_feedback.y):
                        # ended up moving a tile ... check if the board is solved
                        self.checkBoardSolved()


    def ensureBoardInitialized(self):
        # if self.hole_tile_col_idx == -1:
        #     self.initializeBoard()
        # if not self.board_initialized:
        #     self.initializeBoard()
        if self.board_manager is None:
            self.initializeBoard()


    def startRandomizeBoard(self):
        self.showHideHoleTile(False)
        self.randomize_tiles_step_count = self.init_randomize_tile_step_count
        #self.randomize_can_move_from_dir = -1


    def initializeBoard(self):
        self.dd.log("Creating board ...")
        self.board_manager = BoardManager(self.tile_count)

        # export what has been draw as an image named "boardimg"
        self.board.exportLevelsAsImage("boardimg", True)

        self.board.clear()

        # add a "ref" level and draw the exported image "boardimg" on it (as reference)
        self.board.addLevel("ref", switch_to_it=True)
        self.board.levelOpacity(5)
        self.board.drawImageFile("boardimg")

        for row_tile_idx in range(0, self.tile_count):
            for col_tile_idx in range(0, self.tile_count):
                tile_id = col_tile_idx + row_tile_idx * self.tile_count

                # image_name refers to a tile of the image "boardimg"; e.g. "0!4x4@boardimg" refers to the 0th tile of a 4x4 image named "boardimg"
                image_name = str(tile_id) + "!" + str(self.tile_count) + "x" + str(self.tile_count) + "@boardimg"

                tile_level_id = str(tile_id)
                x = col_tile_idx * self.tile_size
                y = row_tile_idx * self.tile_size

                # add a level that represents a tile ... and switch to it
                self.board.addLevel(tile_level_id, self.tile_size, self.tile_size, True)

                # the tile anchor of the level to the tile position on the board
                self.board.setLevelAnchor(x, y)

                # set the back of the level to the tile image, with board (b:3-gray-round)
                self.board.setLevelBackground("", image_name, "b:3-gray-round")

                #self.boardTileIds[rowTileIdx][colTileIdx] = tileId
                #self.board_tiles[row_tile_idx * self.tile_count + col_tile_idx] = tile_id
                if True:
                    if self.board_manager.board_tiles[row_tile_idx * self.tile_count + col_tile_idx] != tile_id:
                        raise Exception("unexpected tile manager tiles")

        # reorder the "ref" level to the bottom, so that it will be drawn underneath the tiles
        self.board.reorderLevel("ref", "B")

        # self.hole_tile_col_idx = 0
        # self.hole_tile_row_idx = 0
        self.move_tile_col_idx = -1
        self.move_tile_row_idx = -1
        self.randomize_move_tile_in_millis = 300
        self.init_randomize_tile_step_count = 5

        #self.board_initialized = True

        self.dd.log("... done creating board")


    def randomizeTilesStep(self):
        #(to_col_idx, to_row_idx, from_tile_id) = self._randomizeTilesStep()
        (to_col_idx, to_row_idx, from_tile_id) = self.board_manager.randomizeBoardStep()

        from_tile_level_id = str(from_tile_id)
        self.board.switchLevel(from_tile_level_id)
        x = to_col_idx * self.tile_size
        y = to_row_idx * self.tile_size

        # move the anchor of the level to the destination in randomizeMoveTileInMillis
        self.board.setLevelAnchor(x, y, self.randomize_move_tile_in_millis)

        # self.hole_tile_col_idx = from_col_idx
        # self.hole_tile_row_idx = from_row_idx

        # since the tile will be moved to the destination in randomizeMoveTileInMillis, delay randomizeMoveTileInMillis here
        time.sleep_ms(self.randomize_move_tile_in_millis)

        # make sure the tile is at the destination
        self.board.setLevelAnchor(x, y)

    # # TODO: not used
    # def _randomizeTilesStep(self):
    #     can_count = self.checkCanMoveFromDirs(self.randomize_can_move_from_dirs, self.randomize_can_move_from_dir)
    #     self.randomize_can_move_from_dir = self.randomize_can_move_from_dirs[random.randint(0, can_count - 1)]
    #     (from_col_idx, from_row_idx) = self.canMoveFromDirToFromIdxes(self.randomize_can_move_from_dir)
    #     to_col_idx = self.hole_tile_col_idx
    #     to_row_idx = self.hole_tile_row_idx
    #     #fromTileId = self.boardTileIds[fromRowIdx][fromColIdx]
    #     from_tile_id = self.board_tiles[from_row_idx * self.tile_count + from_col_idx]
    #     #from_tile_level_id = str(from_tile_id)
    #     #self.boardTileIds[fromRowIdx][fromColIdx] = self.boardTileIds[self.holeTileRowIdx][self.holeTileColIdx]
    #     self.board_tiles[from_row_idx * self.tile_count + from_col_idx] = self.board_tiles[self.hole_tile_row_idx * self.tile_count + self.hole_tile_col_idx]
    #     #self.boardTileIds[self.holeTileRowIdx][self.holeTileColIdx] = fromTileId
    #     self.board_tiles[self.hole_tile_row_idx * self.tile_count + self.hole_tile_col_idx] = from_tile_id
    #     self.hole_tile_col_idx = from_col_idx
    #     self.hole_tile_row_idx = from_row_idx
    #     return (to_col_idx, to_row_idx, from_tile_id)


    def onBoardDragged(self, x: int, y: int) -> bool:
        tile_moved = False
        if x != -1 and y != -1:
            # dragging
            if self.move_tile_col_idx == -1:
                (colIdx, rowIdx, fromDir, ok) = self.posToHoleTileFromIdxes(x, y)
                if ok:
                    self.move_tile_col_idx = colIdx
                    self.move_tile_row_idx = rowIdx
                    self.move_tile_from_dir = fromDir
                    self.move_tile_delta = 0
                    self.move_tile_ref_x = x
                    self.move_tile_ref_y = y
                    #self.moveTileId = self.boardTileIds[self.moveTileRowIdx][self.moveTileColIdx]
                    self.move_tile_id = self.board_manager.board_tiles[self.move_tile_row_idx * self.tile_count + self.move_tile_col_idx]
            else:
                tile_anchor_x = self.move_tile_col_idx * self.tile_size
                tile_anchor_y = self.move_tile_row_idx * self.tile_size
                #delta = 0
                if self.move_tile_from_dir == 0:
                    delta = x - self.move_tile_ref_x
                    if delta > 0:
                        if delta > self.tile_size:
                            delta = self.tile_size
                        tile_anchor_x += delta
                elif self.move_tile_from_dir == 1:
                    delta = self.move_tile_ref_x - x
                    if delta > 0:
                        if delta > self.tile_size:
                            delta = self.tile_size
                        tile_anchor_x -= delta
                elif self.move_tile_from_dir == 2:
                    delta = y - self.move_tile_ref_y
                    if delta > 0:
                        if delta > self.tile_size:
                            delta = self.tile_size
                        tile_anchor_y += delta
                else:
                    delta = self.move_tile_ref_y - y
                    if delta > 0:
                        if delta > self.tile_size:
                            delta = self.tile_size
                        tile_anchor_y -= delta
                self.board.switchLevel(str(self.move_tile_id))
                self.board.setLevelAnchor(tile_anchor_x, tile_anchor_y)
                self.move_tile_delta = delta
        else:
            # done dragging
            if self.move_tile_col_idx != -1:
                # int tileAnchorX;
                # int tileAnchorY;
                if self.move_tile_delta >= self.tile_size / 3:
                    tile_anchor_x = self.board_manager.hole_tile_col_idx * self.tile_size
                    tile_anchor_y = self.board_manager.hole_tile_row_idx * self.tile_size
                    #prevHoleTileId = self.boardTileIds[self.holeTileRowIdx][self.holeTileColIdx]
                    prev_hole_tile_id = self.board_manager.board_tiles[self.board_manager.hole_tile_row_idx * self.tile_count + self.board_manager.hole_tile_col_idx]
                    #self.boardTileIds[self.holeTileRowIdx][self.holeTileColIdx] = self.boardTileIds[self.moveTileRowIdx][self.moveTileColIdx]
                    self.board_manager.board_tiles[self.board_manager.hole_tile_row_idx * self.tile_count + self.board_manager.hole_tile_col_idx] = self.board_manager.board_tiles[self.move_tile_row_idx * self.tile_count + self.move_tile_col_idx]
                    #self.boardTileIds[self.moveTileRowIdx][self.moveTileColIdx] = prevHoleTileId
                    self.board_manager.board_tiles[self.move_tile_row_idx * self.tile_count + self.move_tile_col_idx] = prev_hole_tile_id
                    self.board_manager.hole_tile_col_idx = self.move_tile_col_idx
                    self.board_manager.hole_tile_row_idx = self.move_tile_row_idx
                else:
                    tile_anchor_x = self.move_tile_col_idx * self.tile_size
                    tile_anchor_y = self.move_tile_row_idx * self.tile_size
                self.board.switchLevel(str(self.move_tile_id))
                self.board.setLevelAnchor(tile_anchor_x, tile_anchor_y)
                tile_moved = True
            self.move_tile_col_idx = -1
            self.move_tile_row_idx = -1
        return tile_moved


    def checkBoardSolved(self) -> bool:
        for row_tile_idx in range(0, self.tile_count):
            for col_tile_idx in range(0, self.tile_count):
                tile_id = col_tile_idx + row_tile_idx * self.tile_count
                #boardTileId = self.boardTileIds[rowTileIdx][colTileIdx]
                board_tile_id = self.board_manager.board_tiles[row_tile_idx * self.tile_count + col_tile_idx]
                if board_tile_id != tile_id:
                    return False
        self.dd.log("***** Board Solved *****")
        self.board.enableFeedback()
        # #ifdef SUGGEST_MAX_DEPTH
        # suggestSelection->disabled(true);
        # suggestSelection->deselect(1);
        # suggestContinuously = false;
        # #endif
        self.showHideHoleTile(True)
        time.sleep_ms(200)
        self.showHideHoleTile(False)
        time.sleep_ms(200)
        self.showHideHoleTile(True)
        self.randomize_move_tile_in_millis -= 50  # randomize faster and faster
        if self.randomize_move_tile_in_millis < 50:
            self.randomize_move_tile_in_millis = 50
        self.init_randomize_tile_step_count += 5  # randomize more and more
        if self.init_randomize_tile_step_count > 100:
            self.init_randomize_tile_step_count = 100
        self.waiting_to_restart_millis = 0
        return True


    # # TODO: should not be used
    # def checkCanMoveFromDirs(self, can_move_from_dirs, prev_can_move_from_dir = -1) -> int:  # prevCanMoveFromDir -1 means no previous direction
    #     can_count = 0
    #     if self.hole_tile_col_idx > 0 and prev_can_move_from_dir != 1:
    #         can_move_from_dirs[can_count] = 0  # 0: left
    #         can_count += 1
    #     if self.hole_tile_col_idx < (self.tile_count - 1) and prev_can_move_from_dir != 0:
    #         can_move_from_dirs[can_count] = 1  # 1: right
    #         can_count += 1
    #     if self.hole_tile_row_idx > 0 and prev_can_move_from_dir != 3:
    #         can_move_from_dirs[can_count] = 2  # 2: up
    #         can_count += 1
    #     if self.hole_tile_row_idx < (self.tile_count - 1) and prev_can_move_from_dir != 2:
    #         can_move_from_dirs[can_count] = 3  # 3: down
    #         can_count += 1
    #     return can_count


    # # TODO: should not be used
    # def canMoveFromDirToFromIdxes(self, can_move_from_dir) -> (int, int):
    #     if can_move_from_dir == 0:
    #         from_col_idx = self.hole_tile_col_idx - 1
    #         from_row_idx = self.hole_tile_row_idx
    #     elif can_move_from_dir == 1:
    #         from_col_idx = self.hole_tile_col_idx + 1
    #         from_row_idx = self.hole_tile_row_idx
    #     elif can_move_from_dir == 2:
    #         from_col_idx = self.hole_tile_col_idx
    #         from_row_idx = self.hole_tile_row_idx - 1
    #     else:
    #         from_col_idx = self.hole_tile_col_idx
    #         from_row_idx = self.hole_tile_row_idx + 1
    #     return (from_col_idx, from_row_idx)


    # TODO: move to manager???
    def posToHoleTileFromDir(self, x: int, y: int) -> int:
        if y >= self.board_manager.hole_tile_row_idx * self.tile_size and y < (self.board_manager.hole_tile_row_idx + 1) * self.tile_size:
            if x < self.board_manager.hole_tile_col_idx * self.tile_size:
                if x < (self.board_manager.hole_tile_col_idx - 1) * self.tile_size:
                    return -1
                else:
                    return 0   # left
        if x >= (self.board_manager.hole_tile_col_idx + 1) * self.tile_size:
            if x >= (self.board_manager.hole_tile_col_idx + 2) * self.tile_size:
                return -1
            else:
                return 1  # right
        if x >= self.board_manager.hole_tile_col_idx * self.tile_size and x < (self.board_manager.hole_tile_col_idx + 1) * self.tile_size:
            if y < self.board_manager.hole_tile_row_idx * self.tile_size:
                if y < (self.board_manager.hole_tile_row_idx - 1) * self.tile_size:
                    return -1
                else:
                    return 2  # up
            if y >= (self.board_manager.hole_tile_row_idx + 1) * self.tile_size:
                if y >= (self.board_manager.hole_tile_row_idx + 2) * self.tile_size:
                    return -1
                else:
                    return 3  # down
        return -1


    # TODO: move to manager???
    def posToHoleTileFromIdxes(self, x: int, y: int) -> (int, int, int, bool):
        col_idx = -1
        row_idx = -1
        from_dir = self.posToHoleTileFromDir(x, y)
        if (from_dir == -1):
            return (col_idx, row_idx, from_dir, False)
        if from_dir == 0:
            col_idx = self.board_manager.hole_tile_col_idx - 1
            row_idx = self.board_manager.hole_tile_row_idx
        elif from_dir == 1:
            col_idx = self.board_manager.hole_tile_col_idx + 1
            row_idx = self.board_manager.hole_tile_row_idx
        elif from_dir == 2:
            col_idx = self.board_manager.hole_tile_col_idx
            row_idx = self.board_manager.hole_tile_row_idx - 1
        else:
            col_idx = self.board_manager.hole_tile_col_idx
            row_idx = self.board_manager.hole_tile_row_idx + 1
        return (col_idx, row_idx, from_dir, True)


    def showHideHoleTile(self, show: bool):
        '''
        show / hide the hole tile, which might not be in position
        '''
        #holeTileId = self.boardTileIds[self.holeTileRowIdx][self.holeTileColIdx]
        hole_tile_id = self.board_manager.board_tiles[self.board_manager.hole_tile_row_idx * self.tile_count + self.board_manager.hole_tile_col_idx]
        hole_tile_level_id = str(hole_tile_id)
        anchor_x = self.board_manager.hole_tile_col_idx * self.tile_size
        anchor_y = self.board_manager.hole_tile_row_idx * self.tile_size
        self.board.switchLevel(hole_tile_level_id)
        self.board.setLevelAnchor(anchor_x, anchor_y)
        self.board.setLevelAnchor(0, 0)
        self.board.levelTransparent(not show)


