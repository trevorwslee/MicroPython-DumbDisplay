from .ddimpl import DumbDisplayImpl
from .ddlayer import DDLayer
from .ddlayer import _DD_COLOR_ARG, _DD_BOOL_ARG, _DD_INT_ARG, _DD_FLOAT_ARG


class DDLayerJoystick(DDLayer):
  """Virtual joystick"""
  def __init__(self, dd: DumbDisplayImpl, max_stick_value: int = 1023, directions: str = "", stick_look_scale_factor: float = 1.0):
    """
    :param dd: DumbDisplay object
    :param max_stick_value: the max value of the stick; e.g. 255 or 1023 (the default); min is 15
    :param directions: "lr" or "hori": left-to-right; "tb" or "vert": top-to-bottom; "rl": right-to-left; "bt": bottom-to-top;
                        use "+" combines the above like "lr+tb" to mean both directions; "" the same as "lr+tb"
    :param stick_look_scale_factor: the scaling factor of the stick (UI); 1 by default                    
    """
    layer_id = dd._createLayer("joystick", _DD_INT_ARG(max_stick_value), directions, _DD_FLOAT_ARG(stick_look_scale_factor))
    super().__init__(dd, layer_id)
  def autoRecenter(self, auto_recenter: bool = True):
    self.dd._sendCommand(self.layer_id, "autorecenter", _DD_BOOL_ARG(auto_recenter))
  def colors(self, stick_color: str = "", stick_outline_color: str = "", socket_color: str = "", socket_outline_color = ""):
    self.dd._sendCommand(self.layer_id, "colors", _DD_COLOR_ARG(stick_color), _DD_COLOR_ARG(stick_outline_color), _DD_COLOR_ARG(socket_color), _DD_COLOR_ARG(socket_outline_color))
  def moveToPos(self, x: int, y: int, send_feedback: bool = False):
    """
    move joystick position (if joystick is single directional, will only move in the movable direction)
    :param bg_color: "" means default
    :param x: x to move to
    :param y: y to move to
    :param send_feedback: if true, will send "feedback" for the move (regardless of the current position)
    """
    self.dd._sendCommand(self.layer_id, "movetopos", str(x), str(y), _DD_BOOL_ARG(send_feedback))
  def moveToCenter(self, send_feedback: bool = False):
    """
    move joystick to the center
    :param send_feedback: if true, will send "feedback" for the move (regardless of the current position)
    """
    self.dd._sendCommand(self.layer_id, "movetocenter", _DD_BOOL_ARG(send_feedback))
  def valueRange(self, min_value: int, max_value: int, value_step: int = 1, send_feedback: bool = False):
    """
    set stick max value; will also move the joystick position to "home" -- center if auto-recenter else (0, 0)
    :param min_value the min value of the stick
    :param max_value the max value of the stick
    :param send_feedback if true, will send "feedback" for the move (regardless of the current position)
    """
    self.dd._sendCommand(self.layer_id, "valuerange", _DD_INT_ARG(min_value), _DD_INT_ARG(max_value), _DD_INT_ARG(value_step), _DD_BOOL_ARG(send_feedback))
  def snappy(self, snappy: bool = True):
    """set 'snappy' makes stick snaps to closest value when moved"""
    self.dd._sendCommand(self.layer_id, "snappy", _DD_BOOL_ARG(snappy))
  def showValue(self, show: bool = True, color: str = ""):
    """show value on top of the stick"""
    self.dd._sendCommand(self.layer_id, "showvalue", _DD_BOOL_ARG(show), color)



