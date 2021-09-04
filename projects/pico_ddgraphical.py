from dumbdisplay.uart_io import *
from ._ddgraphical import run as ddgRun

from machine import UART, Pin

def run():
  uart = UART(id=0, baudrate=115200, rx=Pin(1), tx=Pin(0))
  ddgRun(io4Uart(uart), 25)

