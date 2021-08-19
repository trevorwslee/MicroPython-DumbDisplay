import time

def runUart():
  import projects.uart_test as ut
  ut.run()

def runGraphical():
    import projects.ddgraphical as ddg
    ddg.run()
    time.sleep(10)

def runGraphicalBle():
  import projects.ddgraphical as ddg
  ddg.runBle()
  time.sleep(10)

def runGraphicalUart():
  import projects.ddgraphical as ddg
  ddg.runUart()
  time.sleep(10)


def runDebug():
    import u_debug
    u_debug.loop()


if True:
  print("import main")
  print(". main.runDebug()")
  print(". main.runGraphical()")
  print(". main.runGraphicalBle()")
  print(". main.runGraphicalUart()")
  print(". main.runUart()")
else:
  runDebug()
