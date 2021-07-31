import network


from ddio import DDSocketIO


class DDWiFiServerIO(DDSocketIO):
  def __init__(self, ssid, password, port = 10201):
    super().__init__(port)
    print('connecting WIFI ... {} ...'.format(ssid))
    station = network.WLAN(network.STA_IF)
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


