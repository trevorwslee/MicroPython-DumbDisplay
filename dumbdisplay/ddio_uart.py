
from .ddiobase import *


from machine import UART, Pin


# e.g.
# from dumbdisplay.io_uart import *
# dd = DumbDisplay(io4Uart(id=1, baudrate=115200, rx=9, tx=8))

class DDIOUart(DDInputOutput):
  def __init__(self, uart, desc):
    super().__init__()
    self.uart = uart
    self.desc = desc
  def preconnect(self):
    print(f"connect with UART ({self.desc})")
  def available(self):
    return self.uart.any() > 0
  def read(self):
    return self.uart.read().decode('UTF8')
  def print(self, s):
    self.uart.write(s)
  def close(self):
    pass


def io4Uart(id, baudrate, rx, tx):
  try:
    uart = UART(id, baudrate)
    uart.init(baudrate, rx=rx, tx=tx)
  except:
    uart = UART(id, baudrate=baudrate, rx=Pin(rx), tx=Pin(tx))
  return DDIOUart(uart, {"id": id, "baudrate": baudrate, "rx": rx, "tx": tx})
def io4DefUart(id, baudrate):
  uart = UART(id, baudrate)
  return DDIOUart(uart, "default")


