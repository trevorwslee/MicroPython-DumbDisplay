
from ._ddio_base import *

from machine import UART


class DDIOUart(DDInputOutput):
  def __init__(self, id, baudrate = 115200, tx = None, rx = None):
    '''if specify tx, must also specify rx'''
    super().__init__()
    self.uart = UART(id, baudrate)  
    if tx != None:
      self.uart.init(baudrate, tx = tx, rx = rx)
  def available(self):
    return self.uart.any() > 0
  def read(self):
    return self.uart.read().decode('UTF8')
  def print(self, s):
    self.uart.write(s)
  def close(self):
    pass
  
