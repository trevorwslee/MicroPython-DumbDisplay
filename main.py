if True:
  import dumbdisplay as dd
  d = dd.DumbDisplay(dd.io4Ble("uESP32"))
  d.connect()
elif True:
  print("*************************")
  print("*** : import u_debug as u ")
  print("*** : dd = u.DumbDisplay(u.io4Wifi(u.WIFI_SSID, u.WIFI_PWD)) ")
  print("*** : l = u.LayerLedGrid(dd, 6, 4) ")
  print("*** : l.offColor('gray') ")
  print("*************************")
else:
  import u_debug
  u_debug.run(True)
