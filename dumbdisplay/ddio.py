from .ddiobase import DD_DEF_PORT, DDInputOutput
from .ddio_inet import DDIOInet

# e.g.
# from dumbdisplay.io_wifi import *
# dd = DumbDisplay(io4Wifi(WIFI_SSID, WIFI_PWD))

try:
  from .ddio_wifi import DDIOWifi
except:
  pass

def io4Inet(port: int = DD_DEF_PORT, slow_down: bool = True, send_buffer_size: int = None, recv_buffer_size: int = None) -> DDInputOutput:
  return DDIOInet(port, slow_down=slow_down, send_buffer_size=send_buffer_size, recv_buffer_size=recv_buffer_size)

def io4Wifi(ssid: str = None, password: str = None, port: int = DD_DEF_PORT) -> DDInputOutput:
  return DDIOWifi(ssid, password, port)

def io4WifiOrInet(ssid: str, password: str, port: int = DD_DEF_PORT) -> DDInputOutput:
  try:
    return DDIOWifi(ssid, password, port)
  except:
    return DDIOInet(port)


