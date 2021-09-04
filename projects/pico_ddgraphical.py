from dumbdisplay.io import io4Uart
from ._ddgraphical import run as ddgRun

def run():
  io = io4Uart(id=0, baudrate=115200, rx=1, tx=0)
  ddgRun(io, 25)
  # uart = UART(id=0, baudrate=115200, rx=Pin(1), tx=Pin(0))
  # ddgRun(io4IpcoUart(uart), 25)

