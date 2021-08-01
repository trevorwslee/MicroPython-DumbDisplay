
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
  layer.pixelColor(0xff)
  layer.border(1, 0x223344)
  return layer

def run(loop = False):
  while True:
    dd = start()
    led1 = one(dd)
    lcd = two(dd)
    led2 = one(dd)
    auto_pin = AutoPin('V', AutoPin('H', led1, lcd), led2)
    led1.enableFeedback('fa')
    lcd.enableFeedback('fa')
    led2.enableFeedback('fa')
    auto_pin.pin(dd)
    led1.turnOff()
    led2.turnOn()
    if not loop:
      break
    counter = 10
    while counter > 0:
      lcd.writeCenteredLine('in {}'.format(counter))
      dd.writeComment("... restaring in {} ...".format(counter))
      dd.delay(1)
      counter -= 1
      led1.toggle()
      led2.toggle()
    lcd.writeCenteredLine('restarting')
    led1.clear()
    led1.offColor(0xff0000)
    led2.clear()
    led2.offColor('orange')
    dd.delay(2)
    dd.release()
  return dd

if __name__ == "__main__":
  run(True)