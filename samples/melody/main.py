
from dumbdisplay.core import *
from dumbdisplay.layer_graphical import LayerGraphical
from dumbdisplay.layer_lcd import LayerLcd


TOP_HEIGHT = 30
WIDTH = 14
HEIGHT = 80
BORDER = 1



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


def SetupKey(octiveOffset: int, noteIdx: int) -> LayerGraphical:
    width = WIDTH - 2 * BORDER
    xOffset = noteIdx * WIDTH / 2
    #height
    #bgColor
    isSemi = False
    if noteIdx == 1 or noteIdx == 3 or noteIdx == 6 or noteIdx == 8 or noteIdx == 10:
        height = HEIGHT / 2 + 10
        bgColor = "black"
        isSemi = True
    else:
        height = HEIGHT
        bgColor = "white"
    if noteIdx > 4:
        xOffset += WIDTH / 2
    customData = chr(ord(" ") + octiveOffset) + chr(ord(" ") + noteIdx)
    #customData[0] = '0' + octiveOffset;
    #customData[1] = '0' + noteIdx;
    #customData[2] = 0;
    keyLayer = LayerGraphical(dd, width, height)
    keyLayer.customData = customData
    keyLayer.backgroundColor(bgColor)
    keyLayer.border(BORDER, "gray")
    keyLayer.padding(0)
    #keyLayer->setFeedbackHandler(FeedbackHandler, "f");
    if isSemi:
        #dumbdisplay.reorderLayer(keyLayer, "T");
        pass
    else:
        if noteIdx == 0:
            keyLayer.drawStr(2, HEIGHT - 15, "C", "blue")
    l = WIDTH + octiveOffset * 7 * WIDTH + xOffset
    t  = TOP_HEIGHT
    w = width + 2 * BORDER
    h = height + 2 * BORDER
    keyLayer.pinLayer(l, t, w, h)
    return keyLayer

def SetupButton(label: str) -> LayerLcd:
    buttonLayer = LayerLcd(dd, 4, 1)
    buttonLayer.writeLine(label, 0, "C")
    buttonLayer.border(1, "darkgray", "round")
    buttonLayer.noBackgroundColor()
    #buttonLayer.setFeedbackHandler(FeedbackHandler, "f");
    return buttonLayer

dd.recordLayerSetupCommands()

dd.configPinFrame(9 * WIDTH, TOP_HEIGHT + HEIGHT)

SetupKey(-1, 11)
for i in range(0, 12):
    SetupKey(0, i)
SetupKey(1, 0)

playLayer = SetupButton("⏯");
restartLayer = SetupButton("⏮");
targetLayer = SetupButton("📱");

dd.pinAutoPinLayers(AutoPin("H", playLayer, restartLayer, targetLayer).build(), 0, 0, 9 * WIDTH, TOP_HEIGHT)

dd.playbackLayerSetupCommands("ddmelody")
