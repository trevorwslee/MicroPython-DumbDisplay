
from dumbdisplay import *

from _my_secret import *

def start():
  disp = DumbDisplay(io4WifiOrInet(WIFI_SSID, WIFI_PWD))
  disp.debugSetup(2)

  explicit_connect = True
  if explicit_connect:
    disp.connect()

    print("connected: " + str(disp._connected))
    print("compatibility: " + str(disp._compatibility))

    disp.writeComment("Connected from uDebug")
    disp.writeComment("Connected from uDebug")

  return disp

def one(disp):
  layer = LedGridDDLayer(disp, 6, 4)
  layer.offColor("lightgray")
  return layer


if __name__ == "__main__":
  disp = start()
  one(disp)
  disp.release()
