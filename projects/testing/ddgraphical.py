from dumbdisplay.io import *
from ._ddgraphical import run as ddgRun

from _my_secret import *


def run():
  ddgRun(io4WifiOrInet(WIFI_SSID, WIFI_PWD))

def runBle():
  ddgRun(io4Ble("ESP32-2"), 2)

def runUart():
  ddgRun(io4Uart(2, 57600, tx = 16, rx = 17), 2)

#run()