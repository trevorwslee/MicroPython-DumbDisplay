from .ddio_socket import *

import socket

class DDIOInet(DDIOSocket):
  """Python Internet connection"""
  def __init__(self, port = DD_DEF_PORT, slow_down: bool = True)
    super().__init__(port, slow_down=slow_down)
    self.ip = self._get_ip()
  def _get_ip(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
      # doesn't even have to be reachable
      s.connect(('10.255.255.255', 1))
      ip = s.getsockname()[0]
    except Exception:
      ip = '127.0.0.1'
    finally:
      s.close()
    return ip
