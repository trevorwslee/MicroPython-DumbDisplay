
from ._ddio_socket import *

import network

class DDIOWifi(DDIOSocket):
  def __init__(self, ssid, password, port = DD_DEF_PORT):
    super().__init__(port)
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
      print('connecting WIFI ... {} ...'.format(ssid))
      if ssid is None:
        raise Exception('SSID not provided')
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


