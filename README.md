DumbDisplay for Micro-Python is still work in progress!

Although it is targeted for Micro-Python, there might still bebuse cases
for full Python environment like Raspberry Pi Zero.

```
from dumbdisplay.core import *
from dumbdisplay.io_wifi import *
from dumbdisplay.layer_ledgrid import *
dd = DumbDisplay(io4Wifi("ssid", "password"))
l = LayerLedGrid(dd)
l.turnOn()
```

If seeing ESP32 brownout detection issue, try 
```
import machine
machine.reset_cause()
```
