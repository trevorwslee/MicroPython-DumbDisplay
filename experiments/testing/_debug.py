from dumbdisplay._ddiobase import DDInputOutput
from dumbdisplay.core import *
from dumbdisplay.layer_ledgrid import *
from dumbdisplay.layer_lcd import *

def start(io: DDInputOutput):
  dd = DumbDisplay(io)
  #dd.debugSetup(2)

  explicit_connect = True
  if explicit_connect:
    #print("connecteding ...")
    dd.connect()
    #print("... connected")

    print("connected: " + str(dd._connected))
    print("compatibility: " + str(dd._compatibility))

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

def _feedbackHandler(layer, type, x, y):
  print(layer.layer_id + "-FB -- " + type + ":" + str(x) + "," + str(y))
#_feedbackHandler = None

def once(dd, loop = True):
  led1 = one(dd)
  lcd = two(dd)
  led2 = one(dd)
  auto_pin = AutoPin('V', AutoPin('H', led1, lcd), led2)
  led1.enableFeedback("fa", lambda layer, type, x, y: layer.toggle(x, y))
  lcd.enableFeedback("fa", _feedbackHandler)
  led2.enableFeedback("fa", _feedbackHandler)
  lcd.backgroundColor('lightgreen')
  auto_pin.pin(dd)
  led1.turnOff()
  led2.turnOn()
  if loop:
    counter = 10
    while counter > 0:
      lcd.writeCenteredLine('in {}'.format(counter))
      dd.writeComment("... restaring in {} ...".format(counter))
      dd.sleep(1)
      counter -= 1
      led1.toggle()
      led2.toggle()
      feedback = led2.getFeedback()
      if feedback is not None:
        print("led2 FB: {}: {},{}".format(feedback.type, feedback.x, feedback.y))
    lcd.writeCenteredLine('restarting')
    led1.clear()
    led1.offColor(0xff0000)
    led2.clear()
    led2.offColor('orange')
def run():
  dd = start()
  once(dd, False)
  return dd

# def loop(startDD = lambda: start()):
#   while True:
#     #dd = start()
#     dd = startDD(io4WifiOrInet(WIFI_SSID, WIFI_PWD))
#     once(dd, True)
#     dd.delay(2)
#     dd.release()
def loop(io: DDInputOutput):
  while True:
    dd = start(io)
    once(dd, True)
    dd.sleep(2)
    dd.release()

