import dumbdisplay as md

from _my_secret import *

def run():
  # create DumbDisplay connected using WIFI or Inet (Python Internet connection)
  dd = md.DumbDisplay(md.io4WifiOrInet(WIFI_SSID, WIFI_PWD))
  dd.debugSetup(2)

  # create 4 graphical [LCD] layers
  l1 = md.LayerGraphical(dd, 150, 101)
  l2 = md.LayerGraphical(dd, 150, 101)
  l3 = md.LayerGraphical(dd, 150, 101)
  l4 = md.LayerGraphical(dd, 150, 101)

  # set fill screen with color
  l1.fillScreen("azure")
  l2.fillScreen("azure")
  l3.fillScreen("azure")
  l4.fillScreen("azure")

  # "auto pin" the 4 layers -- 2 by 2
  md.AutoPin('H', md.AutoPin('V', l1, l2), md.AutoPin('V', l3, l4)).pin(dd)

  # draw triangles
  left = 0
  right = 150
  top = 0
  bottom = 100
  mid = 50
  for i in range(0, 15):
    left += 3
    top += 3
    right -= 3
    bottom -= 3
    x1 = left
    y1 = mid
    x2 = right
    y2 = top
    x3 = right
    y3 = bottom
    r = 25 * i
    g = 255 - (10 * i)
    b = 2 * i
    l1.drawTriangle(x1, y1, x2, y2, x3, y3, md.RGB_COLOR(r, g, b))

    # draw lines
    i = 0
    while True:
      delta = 5 * i
      x1 = 150
      y1 = 0
      x2 = -150 + delta
      y2 = delta
      l2.drawLine(x1, y1, x2, y2, "blue")
      if x2 > 150:
        break
      i += 1

  # draw rectangles
  for i in range(0, 15):
    delta = 3 * i
    x = delta
    y = delta
    w = 150 - 2 * x
    h = 100 - 2 * y
    l3.drawRect(x, y, w, h, "plum")

  # draw circles
  radius = 10
  for i in range(0, 8):
    x = 2 * radius * i
    for j in range(0, 6):
      y = 2 * radius * j
      r = radius
      l4.drawCircle(x, y, r, "teal")
      l4.drawCircle(x + r, y + r, r, "gold", True)


#run()