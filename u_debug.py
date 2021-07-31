
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

def it():
  io = DDWiFiServerIO(_my_wifi_secret.WIFI_SSID, _my_wifi_secret.WIFI_PWD)
  dd = connectDD(io)

  layer = LedGridDDLayer(dd, 4, 2)
  layer.offColor("lightgray")

  return layer

#it()

#io.close()



