
from dumbdisplay import DumbDisplay
from ddio_inet import DDInetIO
from ddlayer_ledgrid import LedGridDDLayer


def connect_test(io):
  dd = DumbDisplay(io)
  dd.connect()

  print(f"connected: {dd._connected}")
  print(f"compatibility: {dd._compatibility}")

  dd.writeComment("Connected from PyDebug")
  dd.writeComment("Connected from PyDebug")

  ledGridLayer = LedGridDDLayer(dd)
  ledGridLayer.turnOn()

  print("That's it!")


io = DDInetIO(10201)

connect_test(io)

io.close()