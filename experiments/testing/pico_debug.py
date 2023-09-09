from ._debug import loop as dbgLoop

from ._picoetc import picoIO as picoIO

def loop():
  dbgLoop(picoIO)

