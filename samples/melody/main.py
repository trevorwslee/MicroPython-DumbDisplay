
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


def FeedbackHandler(layer, type, x, y):
    #print("FeedbackHandler", melodyApp)
    melodyApp.feedbackHandler(layer, type, x, y)


class MelodyApp:

    def __init__(self):
        self.play = False
        self.playToSpeaker = False
        self.restart = False
        self.adhocFreq = -1

        dd.recordLayerSetupCommands()

        dd.configPinFrame(9 * WIDTH, TOP_HEIGHT + HEIGHT)

        self.setupKey(-1, 11)
        for i in range(0, 12):
            self.setupKey(0, i)
        self.setupKey(1, 0)

        self.playLayer = self.setupButton("⏯");
        self.restartLayer = self.setupButton("⏮");
        self.targetLayer = self.setupButton("📱");

        dd.pinAutoPinLayers(AutoPin("H", self.playLayer, self.restartLayer, self.targetLayer).build(), 0, 0, 9 * WIDTH, TOP_HEIGHT)

        dd.playbackLayerSetupCommands("ddmelody")

    def run(self):
        while True:
            dd.timeslice()
            if self.adhocFreq != -1:
                # key on DumbDisplay pressed ...  play the note/tone of the key press
                self.playTone(self.adhocFreq, 200, self.playToSpeaker)
                self.adhocFreq = -1

    def setupKey(self, octaveOffset: int, noteIdx: int) -> LayerGraphical:
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
        #customData = chr(ord(" ") + octiveOffset) + chr(ord(" ") + noteIdx)
        #customData[0] = '0' + octiveOffset;
        #customData[1] = '0' + noteIdx;
        #customData[2] = 0;
        keyLayer = LayerGraphical(dd, width, height)
        keyLayer.octaveOffset = octaveOffset
        keyLayer.noteIdx = noteIdx
        #keyLayer.customData = customData
        keyLayer.backgroundColor(bgColor)
        keyLayer.border(BORDER, "gray")
        keyLayer.padding(0)
        keyLayer.enableFeedback("fa", FeedbackHandler)
        #keyLayer->setFeedbackHandler(FeedbackHandler, "f");
        if isSemi:
            keyLayer.reorderLayer("T")
            pass
        else:
            if noteIdx == 0:
                keyLayer.drawStr(2, HEIGHT - 15, "C", "blue")
        l = WIDTH + octaveOffset * 7 * WIDTH + xOffset
        t  = TOP_HEIGHT
        w = width + 2 * BORDER
        h = height + 2 * BORDER
        keyLayer.pinLayer(l, t, w, h)
        return keyLayer

    def setupButton(self, label: str) -> LayerLcd:
        buttonLayer = LayerLcd(dd, 4, 1)
        buttonLayer.writeLine(label, 0, "C")
        buttonLayer.border(1, "darkgray", "round")
        buttonLayer.noBackgroundColor()
        buttonLayer.enableFeedback("f", FeedbackHandler)
        return buttonLayer

    def feedbackHandler(self, layer, type, x, y):
        print("clicked")
        if layer == self.playLayer:
            self.play = not self.play
            if self.play:
                self.playLayer.backgroundColor("lightgray")
            else:
                self.playLayer.noBackgroundColor()
        elif layer == self.targetLayer:
            self.playToSpeaker = not self.playToSpeaker
            if self.playToSpeaker:
                self.targetLayer.noBackgroundColor()
            else:
                self.targetLayer.backgroundColor("lightgray")
        elif layer == self.restartLayer:
            self.restart = True
        else:
            octaveOffset = layer.octaveOffset
            noteIdx = layer.noteIdx
            freq = self.getNoteFreq(octaveOffset, noteIdx)
            self.adhocFreq = freq

    def getNoteFreq(self, octave, noteIdx):
        n = noteIdx + 12 * octave - 8
        freq = 440.0 * pow(2, n / 12.0);  # 440 is A
        return int(freq + 0.5)

    def playTone(self, freq, duration, playToSpeaker):
# #ifdef SPEAKER_PIN
# if (playToSpeaker) {
#     PlayTone(freq, duration);
# return;
# }
# #endif
        dd.tone(freq, duration)
        dd.delay_ms(duration)

melodyApp = MelodyApp()
melodyApp.run()
