from _ddio_inet import DDInetIO

try:
  from _ddio_wifi import DDWifiIO
  _DD_HAS_WIFI = True
except:
  _DD_HAS_WIFI = False

DD_DEFAULT_PORT = 10201

def io4Inet(port = DD_DEFAULT_PORT):
  return DDInetIO(port)

def io4Wifi(ssid, password, port = DD_DEFAULT_PORT):
  return DDWifiIO(ssid, password, port)

def io4WifiOrInet(ssid, password, port = DD_DEFAULT_PORT):
  if _DD_HAS_WIFI:
    return DDWifiIO(ssid, password, port)
  else:
    return DDInetIO(port)
