import time


def runDebug():
  from projects.testing import debug
  debug.loop()

def runPicoDebug():
  from projects.testing import pico_debug
  pico_debug.loop()


def runG():
    import projects.testing.ddgraphical as ddg
    ddg.run()
    time.sleep(10)

def runBleG():
    import projects.testing.ddgraphical as ddg
    ddg.runBle()
    time.sleep(10)

def runUartG():
    import projects.testing.ddgraphical as ddg
    ddg.runUart()
    time.sleep(10)

def runPicoG():
    import projects.testing.pico_ddgraphical as ddg
    ddg.run()

def runUart():
    import projects.testing.uart_test as ut
    ut.run()


def show():
    print("import test")
    print(". test.runDebug()")
    print(". test.runPicoDebug()")
    print(". test.runG()")
    print(". test.runBleG()")
    print(". test.runUartG()")
    print(". test.runPicoG()")
    print(". test.runUart()")
