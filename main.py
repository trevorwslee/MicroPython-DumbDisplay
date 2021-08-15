import time

def run():
    import dumbdisplay as m
    tunnel = None
    if True:
      print("*** using UART ***")
      dd = m.DumbDisplay(m.io4Uart(2, 57600, tx = 16, rx = 17))
      if True:
        tunnel = m.TunnelBasic(dd, "192.168.0.203:12345")
    else:  
      dd = m.DumbDisplay(m.io4Ble("uESP32"))
    dd.connect()
    l = m.LayerLedGrid(dd, 4, 2)
    l.offColor(0xff00ff)
    while True:
      l.toggle()
      if tunnel != None:
        if tunnel.dd == None:
          dd.writeComment("CLOSED")
        elif tunnel.eof():
          dd.writeComment("EOF")
          tunnel.release()
        else:
          tunnel.writeLine("uHello")
          if tunnel.count() > 0:
            val = tunnel.readLine()
            dd.writeComment("{" + val + "}")
      time.sleep(1)


def runGraphical():
    import mine.ddgraphical as gm
    gm.run()
    time.sleep(10)

def runDebug():
    import u_debug
    u_debug.loop()


#run()  