import time


# import dumbdisplay as m
# dd = m.DumbDisplay(m.io4Inet())
# t = m.Tunnel(dd, "$$ddb_test$$")
# t.write('hello')
# t.release()
# time.sleep(5)


if True:
  import dumbdisplay as m
  if False:
    dd = m.DumbDisplay(m.io4Uart(2, 115200, tx = 16, rx = 17))
  else:  
    dd = m.DumbDisplay(m.io4Ble("uESP32"))
  dd.connect()
  l = m.LayerLedGrid(dd, 4, 2)
  l.offColor(0xff00ff)
  while True:
    l.toggle()
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
