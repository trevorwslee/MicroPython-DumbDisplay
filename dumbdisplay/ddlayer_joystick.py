from .ddimpl import DumbDisplayImpl
from .ddlayer import DDLayer
from .ddlayer import _DD_COLOR_ARG, _DD_BOOL_ARG, _DD_INT_ARG, _DD_FLOAT_ARG


class DDLayerJoystick(DDLayer):
  '''Virtual joystick'''
  def __init__(self, dd: DumbDisplayImpl, maxStickValue: int = 1023, directions: str = "", stickLookScaleFactor: float = 1.0):
    '''
    :param dd: DumbDisplay object
    :param maxStickValue: the max value of the stick; e.g. 255 or 1023 (the default); min is 15
    :param directions: "lr" or "hori": left-to-right; "tb" or "vert": top-to-bottom; "rl": right-to-left; "bt": bottom-to-top;
                        use "+" combines the above like "lr+tb" to mean both directions; "" the same as "lr+tb"
    :param stickLookScaleFactor: the scaling factor of the stick (UI); 1 by default                    
    '''
    layer_id = dd._createLayer("joystick", _DD_INT_ARG(maxStickValue), directions, _DD_FLOAT_ARG(stickLookScaleFactor))
    super().__init__(dd, layer_id)
  def autoRecenter(self, auto_recenter: bool = True):
    self.dd._sendCommand(self.layer_id, "autorecenter", _DD_BOOL_ARG(auto_recenter))
  def colors(self, stick_color: str = "", stick_outline_color: str = "", socket_color: str = "", socket_outline_color = ""):
    self.dd._sendCommand(self.layer_id, "colors", _DD_COLOR_ARG(stick_color), _DD_COLOR_ARG(stick_outline_color), _DD_COLOR_ARG(socket_color), _DD_COLOR_ARG(socket_outline_color))
  def moveToPos(self, x: int, y: int, send_feedback: bool = False):
    '''
    move joystick position (if joystick is single directional, will only move in the movable direction)
    :param bg_color: "" means default
    :param x: x to move to
    :param y: y to move to
    :param send_feedback: if true, will send "feedback" for the move (regardless of the current position)
    '''
    self.dd._sendCommand(self.layer_id, "movetopos", str(x), str(y), _DD_BOOL_ARG(send_feedback))
  def moveToCenter(self, send_feedback: bool = False):
    '''
    move joystick to the center
    :param send_feedback: if true, will send "feedback" for the move (regardless of the current position)
    '''
    self.dd._sendCommand(self.layer_id, "movetocenter", _DD_BOOL_ARG(send_feedback))


