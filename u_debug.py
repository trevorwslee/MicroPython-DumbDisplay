
import dumbdisplay as dd

import _my_wifi_secret

def start():
  io = dd.io4WifiOrInet(_my_wifi_secret.WIFI_SSID, _my_wifi_secret.WIFI_PWD)

  disp = dd.DumbDisplay(io)
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
  layer = dd.LedGridDDLayer(disp, 5, 4)
  layer.offColor("lightgray")
  return layer




