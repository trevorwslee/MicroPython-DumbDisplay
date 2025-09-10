import time
import bluetooth

class BLE():


    def __init__(self, name):

      self._conn_handle = None

      self.name = name
      self.ble = bluetooth.BLE()
      self.ble.active(True)

      # self.led = Pin(2, Pin.OUT)
      # self.timer1 = Timer(0)
      # self.timer2 = Timer(1)
      
      #self._disconnected()
      self.ble.irq(self._ble_irq)
      self._register()
      self._advertiser()


    def _connected(self):
        
      # self.timer1.deinit()
      # self.timer2.deinit()

      print("connected")

    def _disconnected(self):

      # self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(1))
      # time.sleep_ms(200)
      # self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0))

      print("disconnected")
    

    def _ble_irq(self, event, data):

      print("E:" + str(event))

      if event == 1:
        """Central disconnected"""
        self.conn_handle, _, _, = data
        self._connected()
        #self.led(1)
      
      elif event == 2:
        """Central disconnected"""
        conn_handle, _, _, = data
        if conn_handle == self._conn_handle:
          self.conn_handle = None
        self._disconnected()
        self._advertiser()
      
      elif event == 3:#4:
        """New message received"""
        #conn_handle, value_handle, = data
        #print("...")

        buffer = self.ble.gatts_read(self._rx)
        #message = buffer.decode('UTF-8')[:-1]
        message = buffer.decode('UTF-8').strip()
        print(message)
          
        # if received == 'blue_led':
        #     blue_led.value(not blue_led.value())

            
    def _register(self):
        
      # Nordic UART Service (NUS)
      NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
      RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
      TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
          
      BLE_NUS = bluetooth.UUID(NUS_UUID)
      #BLE_RX = (bluetooth.UUID(RX_UUID), bluetooth.FLAG_WRITE)
      #BLE_TX = (bluetooth.UUID(TX_UUID), bluetooth.FLAG_NOTIFY)
      BLE_RX = (bluetooth.UUID(RX_UUID), bluetooth.FLAG_WRITE)
      BLE_TX = (bluetooth.UUID(TX_UUID), bluetooth.FLAG_INDICATE)
          
      BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
      SERVICES = (BLE_UART, )
      ((self._tx, self._rx,), ) = self.ble.gatts_register_services(SERVICES)

      # Increase the size of the rx buffer and enable append mode.
      self.ble.gatts_set_buffer(self._rx, 100, True)      

    def send(self, data):
      self.ble.gatts_notify(0, self._tx, data + '\n')


    def _advertiser(self):
      name = bytes(self.name, 'UTF-8')
      self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)

    def close(self):
      if self._conn_handle is not None:
        self.ble.gap_disconnect(self._conn_handle)
        self._conn_handle = None
      self.ble.active(False)


def run():
  return BLE('uESP32')      