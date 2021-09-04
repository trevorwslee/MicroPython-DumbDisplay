
from ._ddiobase import *


from machine import UART


class DDIOUart(DDInputOutput):
  # def __init__(self, id, baudrate = 115200, tx = None, rx = None):
  #   '''if specify tx, must also specify rx'''
  #   super().__init__()
  #   self.uart = UART(id, baudrate)
  #   if tx != None:
  #     self.uart.init(baudrate, tx = tx, rx = rx)
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
    uart.init(baudrate, rx = rx, tx = tx)
  except:
    uart = UART(id=0, baudrate=115200, rx=Pin(rx), tx=Pin(tx))
  return DDIOUart(id, baudrate, tx, rx)
def io4DefUart(id, baudrate, rx):
  uart = UART(id, baudrate)
  return DDIOUart(uart)

# def io4Uart(id, baudrate = 115200, tx = None, rx = None):
#   '''if specify tx, must also specify rx'''
#   uart = UART(id, baudrate)
#   if tx != None:
#     uart.init(baudrate, tx = tx, rx = rx)
#   return DDIOUart(id, baudrate, tx, rx)
# def io4IpcoUart(uart):
#   return DDIOUart(uart)

