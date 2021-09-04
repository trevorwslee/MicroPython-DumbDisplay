import time


def runDebug():
  from projects import debug
  debug.loop()

def runPicoDebug():
  from projects import pico_debug
  pico_debug.loop()


def runG():
    import projects.ddgraphical as ddg
    ddg.run()
    time.sleep(10)

def runBleG():
  import projects.ddgraphical as ddg
  ddg.runBle()
  time.sleep(10)

def runUartG():
  import projects.ddgraphical as ddg
  ddg.runUart()
  time.sleep(10)

def runPicoG():
  import projects.pico_ddgraphical as ddg
  ddg.run()

def runUart():
  import projects.uart_test as ut
  ut.run()




if True:
  print("import main")
  print(". main.runDebug()")
  print(". main.runPicoDebug()")
  print(". main.runG()")
  print(". main.runBleG()")
  print(". main.runUartG()")
  print(". main.runPicoG()")
  print(". main.runUart()")
else:
  runDebug()
