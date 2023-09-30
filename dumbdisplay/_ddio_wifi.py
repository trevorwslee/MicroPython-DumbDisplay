
from ._ddio_socket import *

import network

class DDIOWifi(DDIOSocket):
  def __init__(self, ssid, password, port = DD_DEF_PORT):
    if ssid is None:
      raise Exception('SSID not provided')
    super().__init__(port)
    self.ssid = ssid
    self.password = password
  def preconnect(self):
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
      print(f"connecting WIFI ... {self.ssid} ...")
      station.active(True)
      station.connect(self.ssid, self.password)
      while not station.isconnected():
        pass
    self.station = station
    self.read_buf = ""
    print('... connected WIFI')
    #print(station.ifconfig())
    self.ip = station.ifconfig()[0]
    super().preconnect()
  def close(self):
    super().close()
    self.station.disconnect()
    self.station.active(False)
    self.station = None


# class DDIOWifi(DDIOSocket):
#   def __init__(self, ssid, password, port = DD_DEF_PORT):
#     super().__init__(port)
#     station = network.WLAN(network.STA_IF)
#     if not station.isconnected():
#       print('connecting WIFI ... {} ...'.format(ssid))
#       if ssid is None:
#         raise Exception('SSID not provided')
#       station.active(True)
#       station.connect(ssid, password)
#       while not station.isconnected():
#         pass
#     self.station = station
#     self.read_buf = ""
#     print('... connected WIFI')
#     #print(station.ifconfig())
#     self.ip = station.ifconfig()[0]
#   def preconnect(self):
#     self.station.active(True)
#     super().preconnect()
#   def close(self):
#     super().close()
#     #self.station.disconnect()
#     self.station.active(False)
#     #self.station = None

