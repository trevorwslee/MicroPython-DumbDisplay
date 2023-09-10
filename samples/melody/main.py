
from dumbdisplay.core import *
from dumbdisplay.layer_graphical import LayerGraphical
from dumbdisplay.layer_lcd import LayerLcd

try:
    # https://docs.micropython.org/en/latest/library/rp2.html
    import machine
    if machine.unique_id() == b'\xe6aA\x04\x03,D+':  # unique_id() is unique to my board 
        SPEAKER_PIN = 5
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
        mov(x, osr)     # waveCount
        pull(block)
        label("loop")
        mov(y, osr)    # halfWaveNumCycles
        set(pins, 1)   # high
        label("high")
        jmp(y_dec, "high")
        mov(y, osr)    # halfWaveNumCycles
        set(pins, 0)   # low
        label("low")
        jmp(y_dec, "low")
        jmp(x_dec, "loop")
        # set(x, 1)
        # mov(isr, x)
        # push()
    sm = rp2.StateMachine(0, wave_prog, freq=100000, set_base=Pin(SPEAKER_PIN))
    sm.active(1)
    def HWPlayTone(freq: int, duration: int):
        halfWaveNumCycles = round((100000.0 / 2) / freq)  # 2 is the number of cycles per half wave
        waveCount = round(duration * freq / 1000.0)
        sm.put(waveCount)
        sm.put(halfWaveNumCycles)
except:
    print("*****")
    print("* No HWPlayTone")
    print("*****")
    HWPlayTone = None


Song   = "G C E C E D C A G G C E C E D G E G E G E C G A C C A G G C E C E D C Z"
Octave = "0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 0 0 0 1 1 1 1 1 1 Z"
Beat   = "2 4 1 1 4 2 4 2 4 2 4 1 1 4 2 8 2 1 1 1 1 4 2 4 1 1 1 4 2 4 1 1 4 2 8 Z"
Lyrics = [
    [
        "4:Amazing",
        "1:Grace",
        "1:How",
        "1:sweet",
        "1:the",
        "1:sound", ],
    [
        "1:That",
        "1:saved",
        "2:a",
        "1:wretch",
        "1:like",
        "1:me", ],
    [
        "1:I",
        "2:once",
        "2:was",
        "1:lost",
        "1:but",
        "2:now",
        "2:am",
        "1:found", ],
    [
        "1:Was",
        "1:blind",
        "2:but",
        "1:now",
        "1:I",
        "1:see", 
    ],
]

BeatSpeed = 300

TOP_HEIGHT = 50
KEY_WIDTH = 14
KEY_HEIGHT = 80
KEY_BORDER = 1


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
        if HWPlayTone:
            HWPlayTone(freq, duration)
    else:
        dd.tone(freq, duration)
    dd.sleep_ms(duration)


def FeedbackHandler(layer, type, x, y):
    melodyApp.feedbackHandler(layer, type, x, y)


class MelodyApp:

    def __init__(self):
        self.play = False
        self.playToSpeaker = False
        self.restart = False
        self.adhocFreq = -1

        dd.recordLayerSetupCommands()

        dd.configPinFrame(9 * KEY_WIDTH, TOP_HEIGHT + KEY_HEIGHT)

        self.setupKey(-1, 11)
        for i in range(0, 12):
            self.setupKey(0, i)
        self.setupKey(1, 0)

        self.playLayer = self.setupButton("⏯")
        self.restartLayer = self.setupButton("⏮")
        self.targetLayer = self.setupButton("📢")
        self.lyricLayer = LayerGraphical(dd, 280, 50)
        self.lyricLayer.margin(2)
        self.lyricLayer.border(2, "blue", "round")
        self.lyricLayer.backgroundColor("lightgray")
        self.lyricLayer.setTextFont("DL::Roboto")  # use the downloaded font Roboto ... https://fonts.google.com/specimen/Roboto

        if not HWPlayTone:
            self.targetLayer.disabled()

        dd.pinAutoPinLayers(
            AutoPin("V",
        AutoPin("H", self.playLayer, self.restartLayer, self.targetLayer),
                self.lyricLayer).build(),
            0, 0, 9 * KEY_WIDTH, TOP_HEIGHT)

        dd.playbackLayerSetupCommands("uddmelody")

    def run(self):
        while True:
            songIdx = 0
            targetLyricI = 0
            targetLyricSkip = 0
            lyricRowIdx = 0
            lyricColIdx = 0
            while True:
                dd.timeslice()
                if self.adhocFreq != -1:
                    # key on DumbDisplay pressed ...  play the note/tone of the key press
                    if not self.play:
                        self.lyricLayer.clear()
                        self.lyricLayer.setCursor(0, 0)
                        self.lyricLayer.setTextColor("blue")
                        self.lyricLayer.print(f" 🎵 {self.adhocFreq}")
                    PlayTone(self.adhocFreq, 200, self.playToSpeaker)
                    self.adhocFreq = -1
                if self.restart:
                    # restarting ... reset restart flag and break out of loop
                    self.restart = False
                    break
                if not self.play:
                    continue

                i = songIdx * 2
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

                # show the lyric
                dd.recordLayerCommands()
                self.lyricLayer.clear()
                self.lyricLayer.setCursor(0, 0)
                lyricRow = Lyrics[lyricRowIdx]
                self.lyricLayer.setTextSize(16)
                for i, lyric in enumerate(lyricRow):
                    if i == targetLyricI:
                        noteCount = int(lyric[0:1])
                        if (noteCount - targetLyricSkip) <= 1:
                            advance = True
                        else:
                            advance = False
                            targetLyricSkip = targetLyricSkip + 1
                        targetLyric = lyric[2:]
                        self.lyricLayer.setTextColor("red")
                    else:
                        self.lyricLayer.setTextColor("blue")
                    lyric = " " + lyric[2:]
                    self.lyricLayer.print(lyric)
                if True:
                    if lyricRowIdx < len(Lyrics) - 1:
                        lyricRow2 = Lyrics[lyricRowIdx + 1]
                        self.lyricLayer.setCursor(0, 25)
                        self.lyricLayer.setTextSize(12)
                        self.lyricLayer.setTextColor("gray")
                        for i, lyric in enumerate(lyricRow2):
                            lyric = " " + lyric[2:]
                            self.lyricLayer.print(lyric)
                else:
                    print("-", targetLyric)
                dd.playbackLayerCommands()
                if advance:
                    if lyricColIdx < len(lyricRow) - 1:
                        lyricColIdx = lyricColIdx + 1
                        targetLyricI = targetLyricI + 1
                        targetLyricSkip = 0
                    else:
                        lyricColIdx = 0
                        targetLyricI = 0
                        targetLyricSkip = 0
                        if lyricRowIdx < len(Lyrics) - 1:
                            lyricRowIdx = lyricRowIdx + 1
                        else:
                            lyricRowIdx = 0

                # play the note/tone
                PlayTone(freq, duration, self.playToSpeaker)

                songIdx = songIdx + 1


    def setupKey(self, octaveOffset: int, noteIdx: int) -> LayerGraphical:
        width = KEY_WIDTH - 2 * KEY_BORDER
        xOffset = noteIdx * KEY_WIDTH / 2
        isSemi = False
        if noteIdx == 1 or noteIdx == 3 or noteIdx == 6 or noteIdx == 8 or noteIdx == 10:
            height = KEY_HEIGHT / 2 + 10
            bgColor = "black"
            isSemi = True
        else:
            height = KEY_HEIGHT
            bgColor = "white"
        if noteIdx > 4:
            xOffset += KEY_WIDTH / 2
        keyLayer = LayerGraphical(dd, width, height)
        keyLayer.octaveOffset = octaveOffset
        keyLayer.noteIdx = noteIdx
        keyLayer.backgroundColor(bgColor)
        keyLayer.border(KEY_BORDER, "gray")
        keyLayer.padding(0)
        keyLayer.enableFeedback("fa", FeedbackHandler)
        if isSemi:
            keyLayer.reorderLayer("T")
            pass
        else:
            if noteIdx == 0:
                keyLayer.drawStr(2, KEY_HEIGHT - 15, "C", "blue")
        l = KEY_WIDTH + octaveOffset * 7 * KEY_WIDTH + xOffset
        t  = TOP_HEIGHT
        w = width + 2 * KEY_BORDER
        h = height + 2 * KEY_BORDER
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
        if layer == self.playLayer:
            self.play = not self.play
            if self.play:
                self.playLayer.backgroundColor("lightgreen")
            else:
                self.playLayer.noBackgroundColor()
        elif layer == self.targetLayer:
            self.playToSpeaker = not self.playToSpeaker
            if self.playToSpeaker:
                self.targetLayer.backgroundColor("lightgreen")
            else:
                self.targetLayer.noBackgroundColor()
        elif layer == self.restartLayer:
            self.restart = True
        else:
            octaveOffset = layer.octaveOffset
            noteIdx = layer.noteIdx
            freq = GetNoteFreq(octaveOffset, noteIdx)
            self.adhocFreq = freq


melodyApp = MelodyApp()
melodyApp.run()
