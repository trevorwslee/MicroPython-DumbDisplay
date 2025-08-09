import random
import time
import math



def _create_demo_dd():
    '''
    Create a DumbDisplay instance for demo purposes.
    If in MicroPython, it will connect using WiFi (***assuming*** `_my_secret.py`).
    If in Python, it will connect using Inet.
    Note that there should be a single DumbDisplay instance for the whole application.
    '''
    from dumbdisplay.dumbdisplay import DumbDisplay
    if DumbDisplay.runningWithMicropython():
        # connect using WIFI:
        # assume a _my_secret.py Python script containing
        #   WIFI_SSID="SSID"
        #   WIFI_PWD="PASSWORD"
        from _my_secret import WIFI_SSID, WIFI_PWD
        from dumbdisplay.io_wifi import io4Wifi
        dd = DumbDisplay(io4Wifi(WIFI_SSID, WIFI_PWD))
    else:
        # connect using Inet (Python Internet connection)
        from dumbdisplay.io_inet import io4Inet
        dd = DumbDisplay(io4Inet())
    return dd


def demo_LayerLedGrid(col_count = 1, row_count = 1, sub_col_count = 1, sub_row_count = 1):
    '''
    Demonstrate LayerLedGrid.
    :param col_count: number of columns in the grid
    :param row_count: number of rows in the grid
    :param sub_col_count: number of sub-columns in each grid cell
    :param sub_row_count: number of sub-rows in each grid cell
    '''
    from dumbdisplay.layer_ledgrid import LayerLedGrid

    # Create a DumbDisplay instance
    dd = _create_demo_dd()

    # Create a LayerLedGrid layer with the specified parameters, and set it up, like border and LED-off color
    l = LayerLedGrid(dd, col_count=col_count, row_count=row_count, sub_col_count= sub_col_count, sub_row_count=sub_row_count)
    l.border(0.05, "blue")  # note that the border size is relative to the layer's dimension characteristic; e.g. an LED of LayerLedGrid
    l.offColor("green")

    while True:
        dd.timeslice()


def demo_LayerLcd():
    from dumbdisplay.layer_lcd import LayerLcd

    # Create a DumbDisplay instance
    dd = _create_demo_dd()

    # Create a LayerLcd layer and set it up, like border
    # By default, the LayerLcd layer is 16 columns (i.e. 16 characters) by 2 rows (i.e. 2 lines)
    l = LayerLcd(dd)
    l.border(1, "blue")  # note that the border size is relative to the layer's dimension characteristic; e.g. a character of LayerLcd

    # Write some text on the LayerLcd layer
    l.writeCenteredLine("Hello There!")
    l.writeCenteredLine("How are you?", y=1)  # y=1 means the second line (0-based index)

    while True:
        dd.timeslice()


def demo_LayerGraphical():
    from dumbdisplay.layer_graphical import LayerGraphical

    # Create a DumbDisplay instance
    dd = _create_demo_dd()

    # Create a LayerGraphical layer and set it up, like background color and border
    # The LayerGraphical layer is 150 pixels wide and 100 pixels high
    # Note that this size is not the size on the DumbDisplay app's canvas
    # All layers will be scaled to fit the DumbDisplay app's canvas, keeping the aspect ratio.
    l = LayerGraphical(dd, 150, 100)
    l.backgroundColor("azure")
    l.border(3, "blue")

    # Draw on the canvas of the LayerGraphical instance
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

    # Create a DumbDisplay instance
    dd = _create_demo_dd()

    # Create a Layer7SegmentRow instance for 3 digits (in a row), and set it up, like border
    l = Layer7SegmentRow(dd, 3)
    l.border(10, "blue")  # note that the border size is relative to the layer's dimension characteristic; e.g. a digit of Layer7SegmentRow

    # Show the number `777` on the Layer7SegmentRow layer
    l.showNumber(777)

    while True:
        dd.timeslice()


def demo_LayerSelection():
    from dumbdisplay.layer_selection import LayerSelection

    # Create a DumbDisplay instance
    dd = _create_demo_dd()

    # Create a LayerSelection instance with 3 horizontal selections and 1 vertical selection, and set it up, like border
    l = LayerSelection(dd, 12, 1, 1, 3)
    l.border(1, "blue")

    # Set labels for each selection
    for selection_idx in range(3):
        l.textCentered(f"Selection {selection_idx + 1}", vert_selection_idx=selection_idx)

    # Set the second selection as selected
    l.selected(True, vert_selection_idx=1)

    while True:
        dd.timeslice()


def demo_LayerPlotter():
    from dumbdisplay.layer_plotter import LayerPlotter

    # Create a DumbDisplay instance
    dd = _create_demo_dd()

    # Create a LayerPlotter layer with a width of 300 pixels and a height of 100 pixels, and set it up, like border and label
    l = LayerPlotter(dd, 300, 100)
    l.border(5, "blue")
    l.label("X", sin="Sin")

    # Feed data to the LayerPlotter layer
    # Note that the timing affects what show on the LayerPlotter layer
    for x in range(1000):
        sin = math.sin(x)
        l.set(x, sin=sin)
        time.sleep(0.8)

    while True:
        dd.timeslice()


def demo_LayerJoystick(maxStickValue: int = 1023, directions: str = ""):
    from dumbdisplay.layer_joystick import LayerJoystick

    # Create a DumbDisplay instance
    dd = _create_demo_dd()

    # Create a LayerJoystick layer with the specified maxStickValue and directions, and set it up, like border and colors
    l = LayerJoystick(dd, maxStickValue=maxStickValue, directions=directions)
    l.border(5, "blue")
    l.colors(stick_color="green", stick_outline_color="darkgreen")

    while True:
        fb = l.getFeedback()
        if fb:
            print(f"* Feedback: {fb.type} at ({fb.x}, {fb.y})")


def demo_AutoPin():
    from dumbdisplay.full import LayerLedGrid, LayerLcd, LayerGraphical, Layer7SegmentRow, LayerSelection, AutoPin

    dd = _create_demo_dd()

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

    # Use AutoPin to automatically pin the layers to the DumbDisplay instance
    # 3 groups vertically:
    # - 2 layers - l_ledgrid and l_lcd
    # - 2 layers - l_selection and l_7segmentrow
    # - 1 layer - l_graphical
    AutoPin('V',
        AutoPin('H', l_ledgrid, l_lcd),
        AutoPin('H', l_selection, l_7segmentrow),
        l_graphical).pin(dd)

    while True:
        dd.timeslice()


def demo_Feedback():
    from dumbdisplay.layer_ledgrid import LayerLedGrid

    num_leds = 3

    dd = _create_demo_dd()

    l = LayerLedGrid(dd, num_leds)
    l.border(0.05, "blue")  # note that the border size is relative to the layer's dimension characteristic; e.g. an LED of LayerLedGrid
    l.onColor("green")
    l.offColor("lightgray")

    # Enable feedback for the layer; when pressed, auto flash the area (the LED)
    l.enableFeedback("fa")

    while True:
        fb = l.getFeedback()
        if fb:
            print(f"* Feedback: {fb.type} at ({fb.x}, {fb.y})")
            l.toggle(x=fb.x, y=fb.y)  # toggle the LED at the feedback position


def demo_Feedback_callback():
    from dumbdisplay.layer_ledgrid import LayerLedGrid

    num_leds = 3

    dd = _create_demo_dd()

    l = LayerLedGrid(dd, num_leds)
    l.border(0.05, "blue")  # note that the border size is relative to the layer's dimension characteristic; e.g. an LED of LayerLedGrid
    l.onColor("darkred")
    l.offColor("lightgray")

    # Enable feedback for the layer; when pressed, auto flash the area (the LED)
    # Notice the `feedback_handler` parameter, which is a callback function that will be called when feedback is received.
    l.enableFeedback("fa", feedback_handler=
        lambda layer, type, x, y, *args:
            print(f"* Feedback: {type} at ({x}, {y})") or
            layer.toggle(x=x, y=y))

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
    app = SlidingPuzzleApp(dd=_create_demo_dd(), suggest_move_from_dir_func=suggest_move_from_dir_func)
    app.run()

def run_mnist_app():
    from dumbdisplay_examples.mnist.mnist_app import MnistApp
    print(f"*** MnistApp ***")
    inference_func = lambda board_manager: random.randint(0, 9)
    app = MnistApp(dd=_create_demo_dd(), inference_func=inference_func)
    app.run()


if __name__ == "__main__":
    demo_AutoPin()

    if True:
        demo_LayerLedGrid(2, 2)
        demo_LayerLcd()
        demo_LayerGraphical()
        demo_Layer7SegmentRow()
        demo_LayerSelection()
        demo_LayerPlotter()
        demo_LayerJoystick(directions="")  # directions can be "", "lr" or "tb"

        demo_AutoPin()
        demo_Feedback()
        demo_Feedback_callback()

        run_passive_blink_app()
        run_sliding_puzzle_app()
        run_mnist_app()
