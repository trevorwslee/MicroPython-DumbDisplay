
from dumbdisplay import DumbDisplay
from dumbdisplay import AutoPin
from dumbdisplay import io4Wifi
from dumbdisplay import io4WifiOrInet
from dumbdisplay import LayerLedGrid
from dumbdisplay import LayerLcd
from dumbdisplay import Layer7SegmentRow

from _my_secret import *

def start():
  dd = DumbDisplay(io4WifiOrInet(WIFI_SSID, WIFI_PWD))
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
  layer = LayerLedGrid(dd, 6, 4)
  layer.offColor("lightgray")
  return layer
def two(disp):
  layer = LayerLcd(disp)
  layer.print('hello')
  layer.pixelColor(0xff)
  layer.border(1, 0x223344)
  return layer

if __name__ == "__main__":
  dd = start()
  #dd.autoPin('V')
  layer1 = one(dd)
  layer2 = two(dd)
  layer3 = one(dd)
  auto_pin = AutoPin('V', AutoPin('H', layer1, layer2), layer3)
  auto_pin.pin(dd)
  dd.release()
