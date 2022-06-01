DumbDisplay for Micro-Python is still work in progress!

Although it is targeted for Micro-Python, there might still bebuse cases
for full Python environment like Raspberry Pi Zero.

```
import dumbdisplay.core as ddc
from dumbdisplay.layer_ledgrid import *
dd = ddc.DumbDisplay(ddio.io4Inet())
l = LayerLedGrid(dd) 
```