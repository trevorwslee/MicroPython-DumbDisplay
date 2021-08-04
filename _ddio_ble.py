
import _ddio_base

import time
import bluetooth


class DDIOBle(_ddio_base.DDInputOutput):
  def __init__(self):
    super().__init__()
    self.ble = None
    self.buffer = None
  def preconnect(self):
    print('waiting for BLE connection ...')
    self.ble = bluetooth.BLE()
    self.ble.active(True)
    self.ble.irq(self._ble_irq)
    self._register()
    self._advertiser()
    while True:
      if self.buffer != None:
        break
      time.sleep_ms(500)
  def available(self):
    pass
  def read(self):
    pass
  def print(self, s):
    pass
  def close(self):
    pass

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

  def _advertiser(self):
    name = bytes(self.name, 'UTF-8')
    self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)
