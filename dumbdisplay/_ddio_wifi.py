
from ._ddio_base import *

import network

class DDIOWifi(DDIOSocket):
  def __init__(self, ssid, password, port = DD_DEFAULT_PORT):
    super().__init__(port)
    print('connecting WIFI ... {} ...'.format(ssid))
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
      station.active(True)
      station.connect(ssid, password)
      while not station.isconnected():
        pass
    self.station = station
    self.read_buf = ""
    print('... connected WIFI')
    #print(station.ifconfig())
    self.ip = station.ifconfig()[0]
  def close(self):
    super().close()
    self.station.disconnect()
    self.station.active(False)
    self.station = None


