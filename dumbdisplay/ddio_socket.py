from .ddiobase import *


import socket

_SOCKET_BLOCKING = False
_BLOCKING_IO_ERROR_BLOCK_TIME = 0.1

class DDIOSocket(DDInputOutput):
  def __init__(self, port: int, slow_down: bool = True):
    self.ip = "???"
    self.port = port
    self.slow_down = slow_down
    self.sock: socket = None
    self.conn: socket = None
  def preconnect(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connecting socket ... listing on {}:{} ...".format(self.ip, self.port))
    host = '' # empty ==> all accepted
    self.sock = s
    self.sock.bind((host, self.port))
    self.sock.listen(0)
    conn, addr = self.sock.accept() # block and wait
    if _SOCKET_BLOCKING:
      conn.setblocking(True)
    else:
      conn.setblocking(False)
    self.conn = conn
    print("... connected {}:{} from {}".format(self.ip, self.port, addr))
    self.read_buf = ""
  def available(self) -> bool:
    if self.read_buf == "":
      if _SOCKET_BLOCKING:
        import select
        readable, _, _ = select.select([self.sock], [], [], 0)
        if readable:
          try:
            data = self.conn.recv(1024) # non-block
            self.read_buf += data.decode('UTF8')
          except:
            pass
      else:
        try:
          data = self.conn.recv(1024) # non-block
          self.read_buf += data.decode('UTF8')
        except:
          pass
    return self.read_buf != ""
  def read(self) -> str:
    s = self.read_buf
    self.read_buf = ""
    return s
    # c = self.read_buf[:1]
    # self.read_buf = self.read_buf[1:]
    # return c
  def print(self, s: str):
    #print("IO: " + s)
    data = bytes(s, 'UTF8')
    if True:
      if self.slow_down:
        all = len(data)
        self._print(data, all)
      else:
        import time
        while True:
          try:
            self.conn.sendall(data)
            break
          except BlockingIOError as e:
            # retry??? what about data already sent???
            time.sleep(0.01)
    else:
      count = 0
      while all > count:
        try:
          count = self.conn.send(data[count:])
        except Exception as e:
          raise e
        # except OSError as e:
        #   if e.args[0] == 11:
        #     pass
        #   else:
        #     raise e
      #self.conn.sendall(data)
  def printBytes(self, bytes_data: bytes):
    if self.slow_down:
      data = bytes_data
      all = len(data)
      self._print(data, all)
    else:
      if False:
        import time
        try:
          self.conn.sendall(bytes_data)
        except BlockingIOError as e:
          time.sleep(0.01)
        except Exception as e:
          raise e
      else:
        self.conn.sendall(bytes_data)
  def _print(self, data, all):
    count = 0
    while all > count:
      if True:
        import time
        try:
          count = self.conn.send(data[count:])
        except BlockingIOError as e:
          if True:
            print("xxx BlockingIOError during send, retrying ...")
          time.sleep(_BLOCKING_IO_ERROR_BLOCK_TIME)
        except Exception as e:
          raise e
      else:
        try:
          count = self.conn.send(data[count:])
        except Exception as e:
          raise e
  def close(self):
    if self.conn is not None:
      self.conn.close()
      self.sock.close()
    self.conn = None
    self.sock = None




