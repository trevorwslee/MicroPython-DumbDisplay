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


class DDAppBase():
    def __init__(self, dd: DumbDisplay):
        self.dd = dd
        self._initialized = False
        self._pending_master_reset = False

    def run(self):
        self.setup()
        while True:
            self.loop()

    def setup(self):
        pass

    def loop(self):
        (connected, reconnecting) = self.dd.connectPassive()
        if connected:
            if not self._initialized:
                self.initializeDD()
                self._initialized = True
            elif reconnecting:
                self.dd.masterReset()
                self._initialized = False
            else:
                self.updateDD()
                if self._pending_master_reset:
                    self.dd.masterReset(keep_connected=True)
                    self._initialized = False
                    self._pending_master_reset = False

    def initializeDD(self):
        raise Exception("must implement initializeDD")

    def updateDD(self):
        pass

    def masterReset(self):
        self._pending_master_reset = True



