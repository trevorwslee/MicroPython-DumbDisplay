
if True:
  print("*************************")
  print("*** : import u_debug as u ")
  print("*** : dd = u.DumbDisplay(u.io4Wifi(u.WIFI_SSID, u.WIFI_PWD)) ")
  print("*** : l = u.LedGridDDLayer(dd, 6, 4) ")
  print("*** : l.offColor('gray') ")
  print("*************************")
else:
  import u_debug_run
