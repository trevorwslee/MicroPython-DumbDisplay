
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
  layer = dumb.LayerLedGrid(dd, 6, 4)
  layer.offColor("lightgray")
  return layer
def two(disp):
  layer = dumb.LayerLcd(disp)
  layer.print('hello')
  layer.pixelColor(dumb.argColor(0xff))
  layer.border(1, dumb.argColor(0x223344))

if __name__ == "__main__":
  dd = start()
  layer = two(dd)
  dd.release()
