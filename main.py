import time


if True:
  import dumbdisplay as m
  tunnel = None
  if True:
    dd = m.DumbDisplay(m.io4Uart(2, 115200, tx = 16, rx = 17))
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
      else:
        tunnel.writeLine("uHello")
        if tunnel.count() > 0:
          val = tunnel.readLine()
          dd.writeComment("{" + val + "}")
    time.sleep(1)
elif True:
  import mine.ddgraphical as gm
  gm.run()
  time.sleep(10)
elif True:
  import u_debug
  u_debug.loop()
else:
  print("*************************")
  print("*** : import u_debug as u ")
  print("*** : dd = u.DumbDisplay(u.io4Wifi(u.WIFI_SSID, u.WIFI_PWD)) ")
  print("*** : l = u.LayerLedGrid(dd, 6, 4) ")
  print("*** : l.offColor('gray') ")
  print("*************************")
