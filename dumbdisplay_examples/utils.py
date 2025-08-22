from dumbdisplay.dumbdisplay import DumbDisplay


def create_example_wifi_dd():
    """
    create example DumbDisplay ... if for MicroPython WiFi connection, assumes _my_secret.py
    """
    if DumbDisplay.runningWithMicropython():
        # connect using WIFI:
        # assume a _my_secret.py Python script containing
        #   WIFI_SSID="SSID"
        #   WIFI_PWD="PASSWORD"
        from _my_secret import WIFI_SSID, WIFI_PWD
        from dumbdisplay.io_wifi import io4Wifi
        dd = DumbDisplay(io4Wifi(WIFI_SSID, WIFI_PWD))
    else:
        # connect using Inet (Python Internet connection)
        from dumbdisplay.io_inet import io4Inet
        dd = DumbDisplay(io4Inet())
    return dd
