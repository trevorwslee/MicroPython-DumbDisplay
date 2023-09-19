
from ._ddio_socket import *

import time
import bluetooth


class DDIOBle(DDInputOutput):
  def __init__(self, name):
    super().__init__()
    self.name = name
    self.ble = bluetooth.BLE()
    self._conn_handle = None
    self._data = None
  def preconnect(self):
    print('waiting for BLE connection to {} ...'.format(self.name))
    self.ble.active(True)
    self.ble.irq(self._ble_irq)
    self._register()
    self._advertiser()
    while True:
      if self._data is not None:
        break
      time.sleep_ms(500)
    print('... BLE connected')
  def available(self):
    return self._data is not None and len(self._data) > 0
  def read(self):
    return self._data.pop(0)
  def print(self, s):
    while len(s) > 0:
      l = len(s)
      if l > 20: # 20 is the normal limit of BLE
        l = 20
      b = s[0:l]
      s = s[l:]
      self.ble.gatts_notify(0, self._tx, b)
      #print(b)
  def close(self):
    if self._conn_handle is not None:
      self.ble.gap_disconnect(self._conn_handle)
      self._conn_handle = None
      self._data = None
    self.ble.active(False)

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
    #self.ble.gatts_set_buffer(self._rx, 100, True)

  def _advertiser(self):
    name = bytes(self.name, 'UTF-8')
    self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)

  def _ble_irq(self, event, data):
    #print("E:" + str(event))

    if event == 1:
      '''Central disconnected'''
      self._conn_handle, _, _, = data
      self._connected()

    elif event == 2:
      '''Central disconnected'''
      conn_handle, _, _, = data
      if conn_handle == self._conn_handle:
        self.conn_handle = None
      self._disconnected()  
      self._advertiser()

    elif event == 3:#4:
      '''New message received'''
      #conn_handle, value_handle, = data
      #print("...")
      buffer = self.ble.gatts_read(self._rx)
      #message = buffer.decode('UTF-8')[:-1]
      message = buffer.decode('UTF-8').strip()
      #print(message)
      if (self._data is not None):
        self._data.append(message + '\n') 
      #print(str(len(self._data)))


  def _connected(self):
    #print('connected')
    self._data = []
  def _disconnected(self):
    #print('disconnected')
    self._data = None

def io4Ble(name):
  return DDIOBle(name)
