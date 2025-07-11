import random
import time
from dumbdisplay.core import *
from dumbdisplay.layer_graphical import LayerGraphical

# create DumbDisplay
if DumbDisplay.runningWithMicropython():
    # connect using WIFI:
    # assume a _my_secret.py Python script containing
    #   WIFI_SSID="SSID"
    #   WIFI_PWD="PASSWORD"
    from _my_secret import *
    from dumbdisplay.io_wifi import *
    dd = DumbDisplay(io4Wifi(WIFI_SSID, WIFI_PWD))
else:
    # connect using Inet (Python Internet connection)
    from dumbdisplay.io_inet import *
    dd = DumbDisplay(io4Inet())


BOARD_SIZE = 400
TILE_COUNT = 4                        # the the sliding puzzle is 4x4; i.e. 16 tiles
TILE_SIZE = BOARD_SIZE / TILE_COUNT


class SlidingPuzzleApp:
    def __init__(self):
        self.board: LayerGraphical = None
        # tells what tile id (basically tile level id) is at what tile position
        board_tile_ids = []
        for _ in range(TILE_COUNT):
            row_tile_ids = []
            for _ in range(TILE_COUNT):
                row_tile_ids.append(-1)
            board_tile_ids.append(row_tile_ids)
        self.boardTileIds = board_tile_ids
        self.waiting_to_restart_millis = -1  # -1 means not waiting
        self.holeTileColIdx = -1  # -1 means board not initialize
        self.holeTileRowIdx = -1
        self.randomizeCanMoveFromDirs = [-1, -1, -1, -1]
        self.randomizeMoveTileInMillis = 0
        self.initRandomizeTileStepCount = 0
        self.randomizeTilesStepCount = 0
        self.randomizeCanMoveFromDir = -1
        self.moveTileColIdx = -1
        self.moveTileRowIdx = -1
        self.moveTileFromDir = -1
        self.moveTileDelta = -1
        self.moveTileRefX = -1
        self.moveTileRefY = -1
        self.moveTileId = -1

    def run(self):
        while True:
            (connected, reconnecting) = dd.connectPassive()
            if connected:
                if self.board is None:
                    self.initializeDD()
                else:
                    self.updateDD()
            elif reconnecting:
                dd.masterReset()
                self.board = None

    def posToHoleTileFromDir(self, x: int, y: int) -> int:
        if y >= self.holeTileRowIdx * TILE_SIZE and y < (self.holeTileRowIdx + 1) * TILE_SIZE:
            if x < self.holeTileColIdx * TILE_SIZE:
                if x < (self.holeTileColIdx - 1) * TILE_SIZE:
                    return -1
                else:
                    return 0   # left
        if x >= (self.holeTileColIdx + 1) * TILE_SIZE:
            if x >= (self.holeTileColIdx + 2) * TILE_SIZE:
                return -1
            else:
                return 1  # right
        if x >= self.holeTileColIdx * TILE_SIZE and x < (self.holeTileColIdx + 1) * TILE_SIZE:
            if y < self.holeTileRowIdx * TILE_SIZE:
                if y < (self.holeTileRowIdx - 1) * TILE_SIZE:
                    return -1
                else:
                    return 2  # up
            if y >= (self.holeTileRowIdx + 1) * TILE_SIZE:
                if y >= (self.holeTileRowIdx + 2) * TILE_SIZE:
                    return -1
                else:
                    return 3  # down
        return -1

    def posToHoleTileFromIdxes(self, x: int, y: int) -> (int, int, int, bool):
        colIdx = -1
        rowIdx = -1
        fromDir = self.posToHoleTileFromDir(x, y)
        if (fromDir == -1):
            return (colIdx, rowIdx, fromDir, False)
        if fromDir == 0:
            colIdx = self.holeTileColIdx - 1
            rowIdx = self.holeTileRowIdx
        elif fromDir == 1:
            colIdx = self.holeTileColIdx + 1
            rowIdx = self.holeTileRowIdx
        elif fromDir == 2:
            colIdx = self.holeTileColIdx
            rowIdx = self.holeTileRowIdx - 1
        else:
            colIdx = self.holeTileColIdx
            rowIdx = self.holeTileRowIdx + 1
        return (colIdx, rowIdx, fromDir, True)

    def onBoardDragged(self, x: int, y: int) -> bool:
        tileMoved = False
        if x != -1 and y != -1:
            # dragging
            if self.moveTileColIdx == -1:
                (colIdx, rowIdx, fromDir, ok) = self.posToHoleTileFromIdxes(x, y)
                if ok:
                    self.moveTileColIdx = colIdx
                    self.moveTileRowIdx = rowIdx
                    self.moveTileFromDir = fromDir
                    self.moveTileDelta = 0
                    self.moveTileRefX = x
                    self.moveTileRefY = y
                    self.moveTileId = self.boardTileIds[self.moveTileRowIdx][self.moveTileColIdx]
            else:
                tileAnchorX = self.moveTileColIdx * TILE_SIZE
                tileAnchorY = self.moveTileRowIdx * TILE_SIZE
                #delta = 0
                if self.moveTileFromDir == 0:
                    delta = x - self.moveTileRefX
                    if delta > 0:
                        if delta > TILE_SIZE:
                            delta = TILE_SIZE
                        tileAnchorX += delta
                elif self.moveTileFromDir == 1:
                    delta = self.moveTileRefX - x
                    if delta > 0:
                        if delta > TILE_SIZE:
                            delta = TILE_SIZE
                        tileAnchorX -= delta
                elif self.moveTileFromDir == 2:
                    delta = y - self.moveTileRefY
                    if delta > 0:
                        if delta > TILE_SIZE:
                            delta = TILE_SIZE
                        tileAnchorY += delta
                else:
                    delta = self.moveTileRefY - y
                    if delta > 0:
                        if delta > TILE_SIZE:
                            delta = TILE_SIZE
                        tileAnchorY -= delta
                self.board.switchLevel(str(self.moveTileId))
                self.board.setLevelAnchor(tileAnchorX, tileAnchorY)
                self.moveTileDelta = delta
        else:
            # done dragging
            if self.moveTileColIdx != -1:
                # int tileAnchorX;
                # int tileAnchorY;
                if self.moveTileDelta >= TILE_SIZE / 3:
                    tileAnchorX = self.holeTileColIdx * TILE_SIZE
                    tileAnchorY = self.holeTileRowIdx * TILE_SIZE
                    prevHoleTileId = self.boardTileIds[self.holeTileRowIdx][self.holeTileColIdx]
                    self.boardTileIds[self.holeTileRowIdx][self.holeTileColIdx] = self.boardTileIds[self.moveTileRowIdx][self.moveTileColIdx]
                    self.boardTileIds[self.moveTileRowIdx][self.moveTileColIdx] = prevHoleTileId
                    self.holeTileColIdx = self.moveTileColIdx
                    self.holeTileRowIdx = self.moveTileRowIdx
                else:
                    tileAnchorX = self.moveTileColIdx * TILE_SIZE
                    tileAnchorY = self.moveTileRowIdx * TILE_SIZE
                self.board.switchLevel(str(self.moveTileId))
                self.board.setLevelAnchor(tileAnchorX, tileAnchorY)
                tileMoved = True
            self.moveTileColIdx = -1
            self.moveTileRowIdx = -1
        return tileMoved

    def checkBoardSolved(self) -> bool:
        for rowTileIdx in range(0, TILE_COUNT):
            for colTileIdx in range(0, TILE_COUNT):
                tileId = colTileIdx + rowTileIdx * TILE_COUNT
                boardTileId = self.boardTileIds[rowTileIdx][colTileIdx]
                if boardTileId != tileId:
                    return False
        dd.log("***** Board Solved *****")
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
        self.randomizeMoveTileInMillis -= 50  # randomize faster and faster
        if self.randomizeMoveTileInMillis < 50:
            self.randomizeMoveTileInMillis = 50
        self.initRandomizeTileStepCount += 5  # randomize more and more
        if self.initRandomizeTileStepCount > 100:
            self.initRandomizeTileStepCount = 100
        self.waitingToRestartMillis = 0
        return True

    def initializeDD(self):
        board = LayerGraphical(dd, BOARD_SIZE, BOARD_SIZE)
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
        self.holeTileColIdx = -1
        self.holeTileRowIdx = -1
        self.randomizeTilesStepCount = 0
        self.waitingToRestartMillis = 0

    def updateDD(self):
        if self.waitingToRestartMillis != -1:
            # starts off waiting for double tab
            nowMillis = time.ticks_ms()
            diffMillis = nowMillis - self.waitingToRestartMillis
            if diffMillis > 15000:
                dd.log("! double tab to start !")
                self.waitingToRestartMillis = nowMillis

        boardFeedback = self.board.getFeedback()  # ensure the board feedback is updated
        if self.randomizeTilesStepCount > 0:
            # randomizing the board
            self.randomizeTilesStep()
            self.randomizeTilesStepCount -= 1
            if self.randomizeTilesStepCount == 0:
                # randomization is done
                dd.log("... done randomizing board")
                self.board.enableFeedback(":drag")  # :drag to allow dragging that produces MOVE feedback type (and ended with -1, -1 MOVE feedbackv)
        else:
            if boardFeedback is not None:
                if boardFeedback.type == "doubleclick":
                    # double click ==> randomize the board, even during play
                    self.board.flash()
                    self.board.disableFeedback()
                    self.ensureBoardInitialized()
                    dd.log("Randomizing board ...")
                    self.waitingToRestartMillis = -1
                    self.startRandomizeBoard()
                    return
                elif boardFeedback.type == "move":
                    # dragging / moving a tile ... handle it in onBoardDragged
                    if self.onBoardDragged(boardFeedback.x, boardFeedback.y):
                        # ended up moving a tile ... check if the board is solved
                        self.checkBoardSolved()

    def ensureBoardInitialized(self):
        if self.holeTileColIdx == -1:
            self.initializeBoard()

    def startRandomizeBoard(self):
        self.showHideHoleTile(False)
        self.randomizeTilesStepCount = self.initRandomizeTileStepCount
        self.randomizeCanMoveFromDir = -1

    def checkCanMoveFromDirs(self, canMoveFromDirs, prevCanMoveFromDir = -1) -> int:  # prevCanMoveFromDir -1 means no previous direction
        canCount = 0
        if self.holeTileColIdx > 0 and prevCanMoveFromDir != 1:
            canMoveFromDirs[canCount] = 0  # 0: left
            canCount += 1
        if self.holeTileColIdx < (TILE_COUNT - 1) and prevCanMoveFromDir != 0:
            canMoveFromDirs[canCount] = 1  # 1: right
            canCount += 1
        if self.holeTileRowIdx > 0 and prevCanMoveFromDir != 3:
            canMoveFromDirs[canCount] = 2  # 2: up
            canCount += 1
        if self.holeTileRowIdx < (TILE_COUNT - 1) and prevCanMoveFromDir != 2:
            canMoveFromDirs[canCount] = 3  # 3: down
            canCount += 1
        return canCount

    def canMoveFromDirToFromIdxes(self, canMoveFromDir) -> (int, int):
        if canMoveFromDir == 0:
            fromColIdx = self.holeTileColIdx - 1
            fromRowIdx = self.holeTileRowIdx
        elif canMoveFromDir == 1:
            fromColIdx = self.holeTileColIdx + 1
            fromRowIdx = self.holeTileRowIdx
        elif canMoveFromDir == 2:
            fromColIdx = self.holeTileColIdx
            fromRowIdx = self.holeTileRowIdx - 1
        else:
            fromColIdx = self.holeTileColIdx
            fromRowIdx = self.holeTileRowIdx + 1
        return (fromColIdx, fromRowIdx)

    def showHideHoleTile(self, show: bool):
        '''
        show / hide the hole tile, which might not be in position
        '''
        holeTileId = self.boardTileIds[self.holeTileRowIdx][self.holeTileColIdx]
        holeTileLevelId = str(holeTileId)
        anchorX = self.holeTileColIdx * TILE_SIZE
        anchorY = self.holeTileRowIdx * TILE_SIZE
        self.board.switchLevel(holeTileLevelId)
        self.board.setLevelAnchor(anchorX, anchorY)
        self.board.setLevelAnchor(0, 0)
        self.board.levelTransparent(not show)

    def initializeBoard(self):
        dd.log("Creating board ...")

        # export what has been draw as an image named "boardimg"
        self.board.exportLevelsAsImage("boardimg", True)

        self.board.clear()

        # add a "ref" level and draw the exported image "boardimg" on it (as reference)
        self.board.addLevel("ref", switch_to_it=True)
        self.board.levelOpacity(5)
        self.board.drawImageFile("boardimg")

        for rowTileIdx in range(0, TILE_COUNT):
            for colTileIdx in range(0, TILE_COUNT):
                tileId = colTileIdx + rowTileIdx * TILE_COUNT

                # imageName refers to a tile of the image "boardimg"; e.g. "0!4x4@boardimg" refers to the 0th tile of a 4x4 image named "boardimg"
                imageName = str(tileId) + "!" + str(TILE_COUNT) + "x" + str(TILE_COUNT) + "@boardimg"

                tileLevelId = str(tileId)
                x = colTileIdx * TILE_SIZE
                y = rowTileIdx * TILE_SIZE

                # add a level that represents a tile ... and switch to it
                self.board.addLevel(tileLevelId, TILE_SIZE, TILE_SIZE, True)

                # the the tile anchor of the level to the tile position on the board
                self.board.setLevelAnchor(x, y)

                # set the back of the level to the tile image, with board (b:3-gray-round)
                self.board.setLevelBackground("", imageName, "b:3-gray-round")

                self.boardTileIds[rowTileIdx][colTileIdx] = tileId

        # reorder the "ref" level to the bottom, so that it will be drawn underneath the tiles
        self.board.reorderLevel("ref", "B")

        self.holeTileColIdx = 0
        self.holeTileRowIdx = 0
        self.moveTileColIdx = -1
        self.moveTileRowIdx = -1
        self.randomizeMoveTileInMillis = 300
        self.initRandomizeTileStepCount = 5

        dd.log("... done creating board")

    def randomizeTilesStep(self):
        canCount = self.checkCanMoveFromDirs(self.randomizeCanMoveFromDirs, self.randomizeCanMoveFromDir)
        self.randomizeCanMoveFromDir = self.randomizeCanMoveFromDirs[random.randint(0, canCount - 1)]
        (fromColIdx, fromRowIdx) = self.canMoveFromDirToFromIdxes(self.randomizeCanMoveFromDir)
        toColIdx = self.holeTileColIdx
        toRowIdx = self.holeTileRowIdx
        fromTileId = self.boardTileIds[fromRowIdx][fromColIdx]
        fromTileLevelId = str(fromTileId)
        self.boardTileIds[fromRowIdx][fromColIdx] = self.boardTileIds[self.holeTileRowIdx][self.holeTileColIdx]
        self.boardTileIds[self.holeTileRowIdx][self.holeTileColIdx] = fromTileId
        self.board.switchLevel(fromTileLevelId)
        x = toColIdx * TILE_SIZE
        y = toRowIdx * TILE_SIZE

        # move the anchor of the level to the destination in randomizeMoveTileInMillis
        self.board.setLevelAnchor(x, y, self.randomizeMoveTileInMillis)

        self.holeTileColIdx = fromColIdx
        self.holeTileRowIdx = fromRowIdx

        # since the tile will be moved to the destination in randomizeMoveTileInMillis, delay randomizeMoveTileInMillis here
        time.sleep_ms(self.randomizeMoveTileInMillis)

        # make sure the tile is at the destination
        self.board.setLevelAnchor(x, y)


app = SlidingPuzzleApp()
app.run()
