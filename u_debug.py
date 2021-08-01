
import dumbdisplay as dumb

from _my_secret import *

def start():
  dd = dumb.DumbDisplay(dumb.io4WifiOrInet(WIFI_SSID, WIFI_PWD))
  dd.debugSetup(2)

  explicit_connect = True
  if explicit_connect:
    dd.connect()

    print("connected: " + str(dd._connected))
    print("compatibility: " + str(dd._compatibility))

    dd.writeComment("Connected from uDebug")
    dd.writeComment("Connected from uDebug")

  return dd

def one(dd):
  layer = dumb.LedGridDDLayer(dd, 6, 4)
  layer.offColor("lightgray")
  return layer
def two(disp):
  layer = dumb.LcdDDLayer(disp)
  layer.print('hello')
  layer.pixelColor(dumb.layerColor(0xff))

if __name__ == "__main__":
  disp = start()
  two(disp)
  disp.release()
