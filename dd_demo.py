import random
import time
import math


from dumbdisplay_examples.utils import create_example_wifi_dd


def demo_LayerLedGrid(col_count = 1, row_count = 1, sub_col_count = 1, sub_row_count = 1):
    from dumbdisplay.layer_ledgrid import LayerLedGrid
    dd = create_example_wifi_dd()
    l = LayerLedGrid(dd, col_count=col_count, row_count=row_count, sub_col_count= sub_col_count, sub_row_count=sub_row_count)
    l.border(0.05, "blue")
    l.offColor("green")
    while True:
        dd.timeslice()


def demo_LayerLcd():
    from dumbdisplay.layer_lcd import LayerLcd
    dd = create_example_wifi_dd()
    l = LayerLcd(dd)
    l.border(1, "blue")
    l.writeCenteredLine("Hello There!")
    l.writeCenteredLine("How are you?", y=1)
    while True:
        dd.timeslice()


def demo_LayerGraphical():
    from dumbdisplay.layer_graphical import LayerGraphical
    dd = create_example_wifi_dd()
    l = LayerGraphical(dd, 150, 100)
    l.backgroundColor("azure")
    l.border(3, "blue")
    for i in range(0, 15):
        delta = 3 * i
        x = delta
        y = delta
        w = 150 - 2 * x
        h = 100 - 2 * y
        l.drawRect(x, y, w, h, "plum")
    while True:
        dd.timeslice()


def demo_Layer7SegmentRow():
    from dumbdisplay.layer_7segrow import Layer7SegmentRow
    dd = create_example_wifi_dd()
    l = Layer7SegmentRow(dd, 3)
    l.border(10, "blue")
    l.showNumber(777)
    while True:
        dd.timeslice()


def demo_LayerSelection():
    from dumbdisplay.layer_selection import LayerSelection
    dd = create_example_wifi_dd()
    l = LayerSelection(dd, 12, 1, 1, 3)
    l.border(1, "blue")
    for selection_idx in range(3):
        l.textCentered(f"Selection {selection_idx + 1}", vert_selection_idx=selection_idx)
    l.selected(True, vert_selection_idx=1)
    while True:
        dd.timeslice()


def demo_LayerPlotter():
    from dumbdisplay.layer_plotter import LayerPlotter
    dd = create_example_wifi_dd()
    l = LayerPlotter(dd, 300, 100)
    l.border(5, "blue")
    l.label("X", sin="Sin")
    for x in range(1000):
        sin = math.sin(x)
        l.set(x, sin=sin)
        time.sleep(0.8)
    while True:
        dd.timeslice()


def demo_AutoPin():
    from dumbdisplay.full import LayerLedGrid, LayerLcd, LayerGraphical, Layer7SegmentRow, LayerSelection, AutoPin
    dd = create_example_wifi_dd()

    l_ledgrid = LayerLedGrid(dd, 3, 2)
    l_ledgrid.border(0.05, "blue")
    l_ledgrid.offColor("green")

    l_lcd = LayerLcd(dd)
    l_lcd.border(1, "blue")
    l_lcd.writeCenteredLine("Hello There!")
    l_lcd.writeCenteredLine("How are you?", y=1)

    l_7segmentrow = Layer7SegmentRow(dd, 2)
    l_7segmentrow.border(10, "blue")
    l_7segmentrow.showNumber(88)

    l_selection = LayerSelection(dd, 10, 1, 2, 3)
    l_selection.border(1, "blue")
    for selection_idx in range(6):
        l_selection.textCentered(f"Choice {selection_idx + 1}", hori_selection_idx=selection_idx)
    l_selection.selected(True, 1, 2)

    l_graphical = LayerGraphical(dd, 150, 100)
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

    AutoPin('V', AutoPin('H', l_ledgrid, l_lcd), AutoPin('H', l_selection, l_7segmentrow), l_graphical).pin(dd)

    while True:
        dd.timeslice()


def run_passive_blink_app():
    from dumbdisplay_examples.passive_blink.passive_blink_app import PassiveBlinkApp
    print(f"*** PassiveBlinkApp ***")
    app = PassiveBlinkApp()
    app.run()


def run_sliding_puzzle_app():
    from dumbdisplay_examples.sliding_puzzle.sliding_puzzle_app import SlidingPuzzleApp
    print(f"*** SlidingPuzzleApp ***")
    suggest_move_from_dir_func = lambda board_manager: random.randint(0, 3)
    app = SlidingPuzzleApp(dd=create_example_wifi_dd(), suggest_move_from_dir_func=suggest_move_from_dir_func)
    app.run()

def run_mnist_app():
    from dumbdisplay_examples.mnist.mnist_app import MnistApp
    print(f"*** MnistApp ***")
    inference_func = lambda board_manager: random.randint(0, 9)
    app = MnistApp(dd=create_example_wifi_dd(), inference_func=inference_func)
    app.run()


if __name__ == "__main__":
    # test_LayerLedGrid(2, 2)
    # test_LayerLcd()
    # test_LayerGraphical()
    # test_Layer7SegmentRow()
    # test_LayerSelection()
    # test_LayerPlotter()

    demo_AutoPin()

    # run_passive_blink_app()
    # run_sliding_puzzle_app()
    # run_mnist_app()
