import socket

DD_DEFAULT_PORT = 10201

class DDInputOutput:
  def __init__(self):
    pass
  def preconnect(self):
    pass
  def available(self):
    pass
  def read(self):
    pass
  def print(self, s):
    pass
  def close(self):
    pass

class DDSocketIO(DDInputOutput):
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
    self.sock.listen(1)
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
    c = self.read_buf[:1]
    self.read_buf = self.read_buf[1:]
    return c
  def print(self, s):
    data = bytes(s, 'UTF8')
    self.conn.sendall(data)
  def close(self):
    self.conn.close()
    self.sock.close()
    self.conn = None
    self.sock = None




