from ._debug import loop as dbgLoop

from dumbdisplay.io_wifi_or_inet import *

from _my_secret import *

def loop():
  dbgLoop(io4WifiOrInet(WIFI_SSID, WIFI_PWD))

if __name__ == "__main__":
  loop()

