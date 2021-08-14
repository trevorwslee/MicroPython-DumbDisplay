import time


# import dumbdisplay as m
# dd = m.DumbDisplay(m.io4Inet())
# t = m.Tunnel(dd, "$$ddb_test$$")
# t.write('hello')
# t.release()
# time.sleep(5)

# import samples.ddgraphical as sam
# sam.run()

if False:
  import u_debug
  import dumbdisplay as dump
  dd = dump.DumbDisplay(dump.io4Ble("uESP32"))
  dd.connect()
  l = dump.LayerLedGrid(dd, 4, 2)
  l.offColor(0xff00ff)
  while True:
    l.toggle()
    time.sleep(1)
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
