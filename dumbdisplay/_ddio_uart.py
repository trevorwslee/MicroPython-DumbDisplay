
from ._ddiobase import *


from machine import UART, Pin


class DDIOUart(DDInputOutput):
  def __init__(self, uart):
    super().__init__()
    self.uart = uart
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
    uart = UART(id=id, baudrate=baudrate, rx=Pin(rx), tx=Pin(tx))
  return DDIOUart(uart)
def io4DefUart(id, baudrate, rx):
  uart = UART(id, baudrate)
  return DDIOUart(uart)


