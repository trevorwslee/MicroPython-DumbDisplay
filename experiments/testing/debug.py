from ._debug import loop as dbgLoop

from dumbdisplay.io_wifi_or_inet import *

from _my_secret import *

def loop():
  dbgLoop(io4WifiOrInet(WIFI_SSID, WIFI_PWD))

def loopBlePriority(ble_name: str):
  try:
    from dumbdisplay.io_ble import io4Ble
    io = io4Ble(ble_name)
  except:
    io = io4WifiOrInet(WIFI_SSID, WIFI_PWD)  
  dbgLoop(io)


if __name__ == "__main__":
  loop()

