
from dumbdisplay.core import *
from dumbdisplay.io_inet import *
from dumbdisplay.layer_ledgrid import *

dd = DumbDisplay(io4Inet())
l = LayerLedGrid(dd, 20, 20)
l.enableFeedback("fa")
l.offColor(RGB_COLOR(0xcc, 0xcc, 0xcc))
while True:
    feedback = l.getFeedback()
    if feedback != None:
        print("l FB: {}: {},{}".format(feedback.type, feedback.x, feedback.y))
        l.toggle(feedback.x, feedback.y)
