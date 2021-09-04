import time


def runDebug():
  from projects import debug
  debug.loop()

def runPicoDebug():
  from projects import pico_debug
  pico_debug.loop()


def runDD():
    import projects.ddgraphical as ddg
    ddg.run()
    time.sleep(10)

def runBleDD():
  import projects.ddgraphical as ddg
  ddg.runBle()
  time.sleep(10)

def runUartDD():
  import projects.ddgraphical as ddg
  ddg.runUart()
  time.sleep(10)

def runPicoDD():
  import projects.pico_ddgraphical as ddg
  ddg.run()

def runUart():
  import projects.uart_test as ut
  ut.run()




if True:
  print("import main")
  print(". main.runDebug()")
  print(". main.runIpcoDebug()")
  print(". main.runDD()")
  print(". main.runBleDD()")
  print(". main.runUartDD()")
  print(". main.runPicoDD()")
  print(". main.runUart()")
else:
  runDebug()
