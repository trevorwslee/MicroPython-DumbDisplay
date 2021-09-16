from ._debug import loop as dbgLoop

from dumbdisplay.io import io4Uart

picoIO = io4Uart(id=1, baudrate=115200, rx=9, tx=8)
#picoIO = io4Uart(id=0, baudrate=115200, rx=1, tx=0)

