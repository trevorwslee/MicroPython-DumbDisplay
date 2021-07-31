
from dumbdisplay import DumbDisplay
from ddio_debug import DDDebugIO
from ddio_inet import DDInetIO


def connect_test(io):
  dd = DumbDisplay(io)
  dd.connect()

  print(f"connected: {dd._connected}")
  print(f"compatibility: {dd._compatibility}")

  dd.writeComment("Connected from PyDebug")
  dd.writeComment("Connected from PyDebug")

  print("That's it!")


debug_io = DDDebugIO()
socket_io = DDInetIO(10201)

connect_test(socket_io)

socket_io.close()