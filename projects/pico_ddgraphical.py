from dumbdisplay.ddio import io4IpcoUart
from ._ddgraphical import run as ddgRun

from machine import UART, Pin

def run():
  uart = UART(id=0, baudrate=115200, rx=Pin(1), tx=Pin(0))
  ddgRun(io4IpcoUart(uart), 25)

