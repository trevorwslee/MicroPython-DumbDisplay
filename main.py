import time

def runUart():
  import projects.uart_test as ut
  ut.run()

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

def runDebug():
    from projects import u_debug
    u_debug.loop()


if True:
  print("import main")
  print(". main.runDebug()")
  print(". main.runDD()")
  print(". main.runBleDD()")
  print(". main.runUartDD()")
  print(". main.runPicoDD()")
  print(". main.runUart()")
else:
  runDebug()
