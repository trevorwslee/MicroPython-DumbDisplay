
from dumbdisplay.core import *
from dumbdisplay.io_inet import *
from dumbdisplay.layer_lcd import *
from dumbdisplay.layer_graphical import *


_last_x = -1
_color = "red"

def feedback_handler(layer, type, x, y):
    global _last_x, _last_y, _color
    if layer == l:
        if _last_x != -1:
            l.drawLine(_last_x, _last_y, x, y, _color)
        _last_x = x
        _last_y = y
    else:    
        if layer == l_r:
            _color = "red"
        elif layer == l_g:
            _color = "green"
        elif layer == l_b:
            _color = "blue"            
        _last_x = -1   


dd = DumbDisplay(io4Inet())
l_r = LayerLcd(dd)
l_g = LayerLcd(dd)
l_b = LayerLcd(dd)
l = LayerGraphical(dd, 150, 100)
l_r.backgroundColor("red")
l_g.backgroundColor("green")
l_b.backgroundColor("blue")
l.backgroundColor("white")
l.border(3, "black")
l_r.enableFeedback("f", feedback_handler)
l_g.enableFeedback("f", feedback_handler)
l_b.enableFeedback("f", feedback_handler)
l.enableFeedback("fs:rpt50", feedback_handler)
AutoPin('V', AutoPin('H', l_r, l_g, l_b), l).pin(dd)
while True:
    dd.delay(1)



