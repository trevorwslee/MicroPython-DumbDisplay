import time
import dumbdisplay as m

_TRY_RECONNECT = True

def run():
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
        if _TRY_RECONNECT:
          tunnel.reconnect()
        else:
          tunnel.release()
      else:
        tunnel.writeLine("uHello")
        if tunnel.count() > 0:
          val = tunnel.readLine()
          dd.writeComment("{" + val + "}")
    time.sleep(1)


