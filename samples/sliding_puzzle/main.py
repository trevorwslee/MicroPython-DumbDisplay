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


dd.recordLayerSetupCommands()  # this is necessary to enable reconnect

board = LayerGraphical(dd, BOARD_SIZE, BOARD_SIZE)
board.backgroundColor("teal")
board.border(8, "navy", "round", 5)
board.drawRect(0, 0, BOARD_SIZE, BOARD_SIZE, "azure", True)
board.drawRoundRect(20, 20, BOARD_SIZE - 40, BOARD_SIZE - 40, 10, "aqua", True)

board.drawImageFileFit("dumbdisplay.png")
board.setTextFont("DL::Roboto");
board.drawTextLine("In God We Trust", 34, "C", "white", "purple", 32)          # C is for centering on the line (from left to right)
board.drawTextLine("❤️ May God bless you ❤️", 340, "R-20", "purple", "", 20)   # R is for right-justify align on the line; with -20 offset from right

dd.playbackLayerSetupCommands("sliding_puzzle")


while True:
    dd.delay(1)
