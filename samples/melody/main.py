
from dumbdisplay.core import *
from dumbdisplay.layer_graphical import LayerGraphical
from dumbdisplay.layer_lcd import LayerLcd

try:
    # https://docs.micropython.org/en/latest/library/rp2.html
    import time
    import rp2
    from machine import Pin
    @rp2.asm_pio(
        set_init=rp2.PIO.OUT_LOW,
        in_shiftdir=rp2.PIO.SHIFT_LEFT,
        out_shiftdir=rp2.PIO.SHIFT_LEFT,
    )
    def wave_prog():
        pull(block)
        mov(x, osr)  # number of waves
        pull(block)
        label("loop")
        mov(y, osr)  # wave half len number of cycles
        set(pins, 1) # high
        label("high")
        jmp(y_dec, "high")
        mov(y, osr)  # wave half len number of cycles
        set(pins, 0) # low
        label("low")
        jmp(y_dec, "low")
        jmp(x_dec, "loop")
        set(x, 1)
        mov(isr, x)
        push()
    sm = rp2.StateMachine(0, wave_prog, freq=10000, set_base=Pin(15))
    def HWPlayToneBlocked(freq: int, duration: int):
        halfWaveNumCycles = int(10000 / freq / 2)
        waveCount = int(duration / freq / 2)
        #print("halfWaveNumCycles", halfWaveNumCycles)
        #print("waveCount", waveCount)
        sm.active(1)
        start_ms = time.ticks_ms()
        sm.put(waveCount)
        sm.put(halfWaveNumCycles) # 2 * (x / 10) == blink time
        res = sm.get()
        taken_ms = time.ticks_ms() - start_ms
        #print(f"got result {res} in {taken_ms:.2} ms")
        sm.active(0)
except:
    print("*****")
    print("* No HWPlayToneBlocked")
    print("*****")
    HWPlayToneBlocked = None


Song   = "G C E C E D C A G G C E C E D G E G E G E C G A C C A G G C E C E D C Z"
Octave = "0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 0 0 0 1 1 1 1 1 1 Z"
Beat   = "2 4 1 1 4 2 4 2 4 2 4 1 1 4 2 8 2 1 1 1 1 4 2 4 1 1 1 4 2 4 1 1 4 2 8 Z"

BeatSpeed = 300

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


# noteName: C, D, E, F, G, A, B
# halfNote: #, b
def ToNoteIdx(noteName, halfNote):
    if noteName == 'C':
        noteIdx = 0
    elif noteName == 'D':
        noteIdx = 2
    elif noteName == 'E':
        noteIdx = 4
    elif noteName == 'F':
        noteIdx = 5
    elif noteName == 'G':
        noteIdx = 7
    elif noteName == 'A':
        noteIdx = 9
    elif noteName == 'B':
        noteIdx = 11
    if halfNote == '#':
        noteIdx = noteIdx + 1
    elif halfNote == 'b':
        noteIdx = noteIdx - 1
    return noteIdx


# octave: can be negative
# noteIdx: 0 to 11; i.e. 12 note indexes in an octave
def GetNoteFreq(octave, noteIdx):
    n = noteIdx + 12 * octave - 8
    freq = 440.0 * pow(2, n / 12.0)  # 440 is A
    return int(freq + 0.5)


def PlayTone(freq: int, duration: int, playToSpeaker: bool):
    if playToSpeaker:
        if HWPlayToneBlocked:
            HWPlayToneBlocked(freq, duration)
    else:
        dd.tone(freq, duration)
        dd.sleep_ms(duration)


def FeedbackHandler(layer, type, x, y):
    #print("FeedbackHandler", melodyApp)
    melodyApp.feedbackHandler(layer, type, x, y)


class MelodyApp:

    def __init__(self):
        self.play = False
        self.playToSpeaker = HWPlayToneBlocked != None
        self.restart = False
        self.adhocFreq = -1

        dd.recordLayerSetupCommands()

        dd.configPinFrame(9 * WIDTH, TOP_HEIGHT + HEIGHT)

        self.setupKey(-1, 11)
        for i in range(0, 12):
            self.setupKey(0, i)
        self.setupKey(1, 0)

        self.playLayer = self.setupButton("⏯")
        self.restartLayer = self.setupButton("⏮")
        self.targetLayer = self.setupButton("📢")

        if not HWPlayToneBlocked:
            self.targetLayer.disabled()

        dd.pinAutoPinLayers(AutoPin("H", self.playLayer, self.restartLayer, self.targetLayer).build(), 0, 0, 9 * WIDTH, TOP_HEIGHT)

        dd.playbackLayerSetupCommands("ddmelody")

    def run(self):
        while True:
            i = 0
            while True:
                dd.timeslice()
                if self.adhocFreq != -1:
                    # key on DumbDisplay pressed ...  play the note/tone of the key press
                    PlayTone(self.adhocFreq, 200, self.playToSpeaker)
                    self.adhocFreq = -1
                if self.restart:
                    # restarting ... reset restart flag and break out of loop
                    self.restart = False
                    break
                if not self.play:
                    continue
                noteName = Song[i]
                if noteName == "Z":
                    # reached end of song => break out of loop
                    break

                halfNote = Song[i + 1]

                # convert the song note into tone frequency
                noteIdx = ToNoteIdx(noteName, halfNote)
                freq = GetNoteFreq(ord(Octave[i]) - ord('0'), noteIdx)

                # get the how to to play the note/tone for
                duration = BeatSpeed * (ord(Beat[i]) - ord('0'))

                # play the note/tone
                PlayTone(freq, duration, self.playToSpeaker)

                # increment i by 2
                i = i + 2


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
        keyLayer = LayerGraphical(dd, width, height)
        keyLayer.octaveOffset = octaveOffset
        keyLayer.noteIdx = noteIdx
        keyLayer.backgroundColor(bgColor)
        keyLayer.border(BORDER, "gray")
        keyLayer.padding(0)
        keyLayer.enableFeedback("fa", FeedbackHandler)
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
        #print("clicked")
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
            freq = GetNoteFreq(octaveOffset, noteIdx)
            self.adhocFreq = freq


melodyApp = MelodyApp()
melodyApp.run()
