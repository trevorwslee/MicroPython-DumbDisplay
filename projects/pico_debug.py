from ._debug import loop as dbgLoop

from dumbdisplay.io import io4Uart

def loop():
  io = io4Uart(id=0, baudrate=115200, rx=1, tx=0)
  dbgLoop(io)
  # uart = UART(id=0, baudrate=115200, rx=Pin(1), tx=Pin(0))
  # dbgLoop(io4IpcoUart(uart))

