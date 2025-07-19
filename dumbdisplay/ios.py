###
# try import IOs for all types
###

try:
  from .ddio import io4Inet
  from .ddio import io4Wifi
  from .ddio import io4WifiOrInet
except:
  pass

try:
  from .ddio_ble import io4Ble
except:
  pass

try:
  from .ddio_uart import io4Uart
  from .ddio_uart import io4DefUart
except:
  pass
