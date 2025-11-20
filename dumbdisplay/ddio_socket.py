import sys
from .ddiobase import *


import socket

_SOCKET_BLOCKING = False
_BLOCKING_IO_ERROR_BLOCK_TIME = 0.2

class DDIOSocket(DDInputOutput):
  def __init__(self, port: int, slow_down: bool = True, send_buffer_size: int = None, recv_buffer_size: int = None):
    super().__init__()
    self.ip = "???"
    self.port = port
    self.slow_down = slow_down
    self.send_buffer_size = send_buffer_size
    self.recv_buffer_size = recv_buffer_size
    self.sock: socket = None
    self.conn: socket = None
    self.is_for_u_python = hasattr(sys, 'implementation') and sys.implementation.name == 'micropython'
    self.read_buf = None
  def preconnect(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if self.send_buffer_size is not None:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.send_buffer_size)
    if self.recv_buffer_size is not None:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.recv_buffer_size)
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
    if self.send_buffer_size is not None:
        #self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.send_buffer_size)
        send_buffer_size = self.conn.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        print("    . send_buffer_size={} vs {}".format(send_buffer_size, self.send_buffer_size))
    if self.recv_buffer_size is not None:
        #self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.recv_buffer_size)
        recv_buffer_size = self.conn.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        print("    ... recv_buffer_size={} vs {}".format(recv_buffer_size, self.recv_buffer_size))
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
        self._print(data, len(data))
      else:
        while True:
          if self.is_for_u_python:
              raise NotImplementedError("sendall() not implemented for uPython")
          else:  
            try:
              self.conn.sendall(data)
              break
            except BlockingIOError as e:
                send_buffer_size = self.conn.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
                print(f"xxx BlockingIOError during sendall ... send_buffer_size={send_buffer_size}")
                raise
    else:
      raise Exceptipon("not implemented")
      # count = 0
      # while all > count:
      #   try:
      #     count = self.conn.send(data[count:])
      #   except Exception as e:
      #     raise e
      #   # except OSError as e:
      #   #   if e.args[0] == 11:
      #   #     pass
      #   #   else:
      #   #     raise e
      # #self.conn.sendall(data)
  def printBytes(self, bytes_data: bytes):
    if self.slow_down:
      data = bytes_data
      #all = len(data)
      self._print(data, len(data))
    else:
      if True:
          if self.is_for_u_python:
              raise NotImplementedError("sendall() not implemented for uPython")
          else:  
            try:
              self.conn.sendall(bytes_data)
            except BlockingIOError as e:
                send_buffer_size = self.conn.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
                print(f"xxx BlockingIOError during sendall ... send_buffer_size={send_buffer_size}")
                raise
      else:
        self.conn.sendall(bytes_data)
  def _print(self, data, data_len):
    count = 0
    while data_len > count:
      if self.is_for_u_python:
        try:
          count += self.conn.send(data[count:])
        except Exception as e:
          raise e
      else:  
        import time
        try:
          count += self.conn.send(data[count:])
        except BlockingIOError as e:
          if True:
            send_buffer_size = self.conn.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            print(f"xxx BlockingIOError during send, retrying ... send_buffer_size={send_buffer_size}")
          time.sleep(_BLOCKING_IO_ERROR_BLOCK_TIME)
        except Exception as e:
          raise e
  def close(self):
    if self.conn is not None:
      self.conn.close()
      self.sock.close()
    self.conn = None
    self.sock = None




