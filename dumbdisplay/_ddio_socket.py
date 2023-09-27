from ._ddiobase import *


import socket

class DDIOSocket(DDInputOutput):
  def __init__(self, port):
    self.ip = "???"
    self.port = port
    self.sock = None
    self.conn = None
  def preconnect(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connecting socket ... listing on {}:{} ...".format(self.ip, self.port))
    host = '' # empty ==> all accepted
    self.sock = s
    self.sock.bind((host, self.port))
    self.sock.listen(0)
    conn, addr = self.sock.accept() # block and wait
    conn.setblocking(False)
    self.conn = conn
    print("... connected {}:{} from {}".format(self.ip, self.port, addr))
    self.read_buf = ""
  def available(self):
    if self.read_buf == "":
      try:
        data = self.conn.recv(1024) # non-block
        self.read_buf += data.decode('UTF8')
      except:
        pass
    return self.read_buf != ""
  def read(self):
    s = self.read_buf
    self.read_buf = ""
    return s
    # c = self.read_buf[:1]
    # self.read_buf = self.read_buf[1:]
    # return c
  def print(self, s):
    #print("IO: " + s)
    data = bytes(s, 'UTF8')
    all = len(data)
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
  def close(self):
    if self.conn is not None:
      self.conn.close()
      self.sock.close()
    self.conn = None
    self.sock = None




