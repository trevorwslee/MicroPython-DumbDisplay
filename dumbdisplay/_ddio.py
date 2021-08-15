from ._ddiobase import DD_DEFAULT_PORT
from ._ddio_inet import DDIOInet

try:
  from ._ddio_wifi import DDIOWifi
  _DD_HAS_WIFI = True
except:
  _DD_HAS_WIFI = False

try:
  from ._ddio_uart import DDIOUart
except:
  pass    

try:
  from ._ddio_ble import DDIOBle
except:
  pass    

def io4Inet(port = DD_DEFAULT_PORT):
  return DDIOInet(port)

def io4Wifi(ssid, password, port = DD_DEFAULT_PORT):
  return DDIOWifi(ssid, password, port)

def io4WifiOrInet(ssid, password, port = DD_DEFAULT_PORT):
  if _DD_HAS_WIFI:
    return DDIOWifi(ssid, password, port)
  else:
    return DDIOInet(port)


def io4Ble(name):
  return DDIOBle(name)  

def io4Uart(id, baudrate = 115200, tx = None, rx = None):
  return DDIOUart(id, baudrate, tx, rx)   

