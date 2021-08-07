
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
    #print("connecteding ...")
    dd.connect()
    #print("... connected")

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

def once(dd, loop = True):
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
  if loop:
    counter = 10
    while counter > 0:
      lcd.writeCenteredLine('in {}'.format(counter))
      dd.writeComment("... restaring in {} ...".format(counter))
      dd.delay(1)
      counter -= 1
      led1.toggle()
      led2.toggle()
      # feedback = led2.getFeedback()
      # if feedback != None:
      #   type = feedback[0]
      #   x = feedback[1]
      #   y = feedback[2]
      #   print("led2 FB: {}: {},{}".format(type, x, y))
    lcd.writeCenteredLine('restarting')
    led1.clear()
    led1.offColor(0xff0000)
    led2.clear()
    led2.offColor('orange')
def run():
  dd = start()
  once(dd, False)
  return dd

def loop(startDD = lambda: start()):
  while True:
    #dd = start()
    dd = startDD()
    once(dd, True)
    dd.delay(2)
    dd.release()

if __name__ == "__main__":
  loop()