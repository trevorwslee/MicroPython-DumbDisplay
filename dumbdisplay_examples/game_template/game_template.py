import time

from dumbdisplay import *

from dumbdisplay_examples.utils import DDAppBase, create_example_wifi_dd


_delay = 0.1

class GameTemplateApp(DDAppBase):
    def __init__(self, dd: DumbDisplay = create_example_wifi_dd()):
        super().__init__(dd)
        self.wn: LayerTurtle = None
        self.last_update_time = None

    def initializeDD(self):
        self.dd.log("*** creating LayerLedGrid ...")
        l_ledgrid = LayerLedGrid(self.dd, 3, 2)
        l_ledgrid.border(0.05, "blue")
        l_ledgrid.offColor("green")
        l_ledgrid.enableFeedback(":press", lambda layer, type, *args: l_ledgrid.offColor("blue") if type == "down" else l_ledgrid.offColor("green"))
        self.dd.log("*** ... done creating LayerLedGrid")

        self.dd.log("*** creating LayerLcd ...")
        l_lcd = LayerLcd(self.dd)
        l_lcd.border(1, "blue")
        l_lcd.writeCenteredLine("Hello There!")
        l_lcd.writeCenteredLine("How are you?", y=1)
        l_lcd.enableFeedback("fl", lambda layer, type, *args: self.dd.log(f"- detected LCD `{type}`"))
        self.dd.log("*** ... done creating LayerLcd")

        self.dd.log("*** creating Layer7SegmentRow ...")
        l_7segmentrow = Layer7SegmentRow(self.dd, 2)
        l_7segmentrow.border(10, "blue")
        l_7segmentrow.showNumber(88)
        self.dd.log("*** ... done creating Layer7SegmentRow")

        self.dd.log("*** creating LayerSelection ...")
        l_selection = LayerSelection(self.dd, 10, 1, 2, 3)
        l_selection.border(1, "blue")
        for selection_idx in range(6):
            l_selection.textCentered(f"Choice {selection_idx + 1}", hori_selection_idx=selection_idx)
        l_selection.enableFeedback("fa", lambda layer, type, x, y, *args: l_selection.selected(True, x + 2 * y, reverse_the_others=True))
        self.dd.log("*** ... done creating LayerSelection")

        self.dd.log("*** creating LayerGraphical ...")
        l_graphical = LayerGraphical(self.dd, 150, 100)
        l_graphical.backgroundColor("azure")
        l_graphical.border(3, "blue")
        radius = 10
        for i in range(0, 8):
            x = 2 * radius * i
            for j in range(0, 6):
                y = 2 * radius * j
                r = radius
                l_graphical.drawCircle(x, y, r, "teal")
                l_graphical.drawCircle(x + r, y + r, r, "gold", True)
        l_graphical.enableFeedback("fs:drag", lambda layer, type, x, y, *args: self.dd.log(f"- DRAG at ({x},{y})'"))
        self.dd.log("*** ... creating LayerGraphical")

        AutoPin('V',
                AutoPin('H', l_ledgrid, l_lcd),
                AutoPin('H', l_selection, l_7segmentrow),
                l_graphical).pin(self.dd)

        self.last_update_time = time.time()
        self.startGame()

    def updateDD(self):
        now = time.time()
        need_update = (now - self.last_update_time) >= _delay
        if need_update:
            self.last_update_time = now
            self.update()

    def startGame(self):
        pass

    def update(self):
        pass


if __name__ == "__main__":
    from dumbdisplay_examples.utils import create_example_wifi_dd, DDAppBase
    app = GameTemplateApp(create_example_wifi_dd())
    app.run()
