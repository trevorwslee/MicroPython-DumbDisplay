from ._debug import loop as dbgLoop

from dumbdisplay.ddio import io4IpcoUart

from machine import UART, Pin

def loop():
  uart = UART(id=0, baudrate=115200, rx=Pin(1), tx=Pin(0))
  dbgLoop(io4IpcoUart(uart))

