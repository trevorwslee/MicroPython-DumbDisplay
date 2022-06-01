DumbDisplay for Micro-Python is still work in progress!

Although it is targeted for Micro-Python, there might still bebuse cases
for full Python environment like Raspberry Pi Zero.

```
from dumbdislay.core import *
from dumbdisplay.layer_ledgrid import *
dd = DumbDisplay(ddio.io4Inet())
l = LayerLedGrid(dd)
l.turnOn()
```