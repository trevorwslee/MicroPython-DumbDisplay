import time


def runDebug():
  from experiments.testing import debug
  debug.loop()


def runDebugBlePriority(ble_name: str):
  from experiments.testing import debug
  debug.loopBlePriority(ble_name)


def runPicoDebug():
  from experiments.testing import pico_debug
  pico_debug.loop()


def runG():
    import experiments.testing.ddgraphical as ddg
    ddg.run()
    time.sleep(10)

def runBleG():
    import experiments.testing.ddgraphical as ddg
    ddg.runBle()
    time.sleep(10)

def runUartG():
    import experiments.testing.ddgraphical as ddg
    ddg.runUart()
    time.sleep(10)

def runPicoG():
    import experiments.testing.pico_ddgraphical as ddg
    ddg.run()

def runUart():
    import experiments.testing.uart_test as ut
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
