
from dumbdisplay import DumbDisplay
from ddio_wifi import DDWiFiServerIO

import _my_wifi_secret

def connect_test(io):
  dd = DumbDisplay(io)
  dd.debugSetup(2)
  dd.connect()

  print("connected: " + str(dd._connected))
  print("compatibility: " + str(dd._compatibility))

  dd.writeComment("Connected from uDebug")
  dd.writeComment("Connected from uDebug")

  print("That's it!")


io = DDWiFiServerIO(_my_wifi_secret.WiFiSsid, _my_wifi_secret.WifiPassword)

connect_test(io)

io.close()



