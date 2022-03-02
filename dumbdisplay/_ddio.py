from ._ddiobase import DD_DEF_PORT, DDInputOutput
from ._ddio_inet import DDIOInet

try:
  from ._ddio_wifi import DDIOWifi
except:
  pass

def io4Inet(port: int = DD_DEF_PORT) -> DDInputOutput:
  return DDIOInet(port)

def io4Wifi(ssid: str, password: str, port: int = DD_DEF_PORT) -> DDInputOutput:
  return DDIOWifi(ssid, password, port)

def io4WifiOrInet(ssid: str, password: str, port: int = DD_DEF_PORT) -> DDInputOutput:
  try:
    return DDIOWifi(ssid, password, port)
  except:
    return DDIOInet(port)


#
# try:
#   from ._ddio_wifi import DDIOWifi
#   _DD_HAS_WIFI = True
# except:
#   _DD_HAS_WIFI = False
#
# def io4Inet(port = DD_DEF_PORT):
#   return DDIOInet(port)
#
# def io4Wifi(ssid, password, port = DD_DEF_PORT):
#   return DDIOWifi(ssid, password, port)
#
# def io4WifiOrInet(ssid, password, port = DD_DEF_PORT):
#   if _DD_HAS_WIFI:
#     return DDIOWifi(ssid, password, port)
#   else:
#     return DDIOInet(port)


