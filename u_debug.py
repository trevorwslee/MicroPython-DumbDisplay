
from dumbdisplay import DumbDisplay
from ddio_wifi import DDWiFiServerIO
from ddlayer_ledgrid import LedGridDDLayer

import _my_wifi_secret

def connectDD(io):
  dd = DumbDisplay(io)
  dd.debugSetup(2)
  dd.connect()

  print("connected: " + str(dd._connected))
  print("compatibility: " + str(dd._compatibility))

  dd.writeComment("Connected from uDebug")
  dd.writeComment("Connected from uDebug")

  return dd 



def start():
  io = DDWiFiServerIO(_my_wifi_secret.WIFI_SSID, _my_wifi_secret.WIFI_PWD)
  dd = connectDD(io)
  return dd
def one(dd):
  layer = LedGridDDLayer(dd, 5, 4)
  layer.offColor("lightgray")
  return layer


def run():
  return one(start())



