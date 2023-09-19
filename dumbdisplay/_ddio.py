from ._ddiobase import DD_DEF_PORT, DDInputOutput
from ._ddio_inet import DDIOInet

try:
  from ._ddio_wifi import DDIOWifi
except:
  pass

def io4Inet(port: int = DD_DEF_PORT) -> DDInputOutput:
  return DDIOInet(port)

def io4Wifi(ssid: str = None, password: str = None, port: int = DD_DEF_PORT) -> DDInputOutput:
  return DDIOWifi(ssid, password, port)

def io4WifiOrInet(ssid: str, password: str, port: int = DD_DEF_PORT) -> DDInputOutput:
  try:
    return DDIOWifi(ssid, password, port)
  except:
    return DDIOInet(port)


