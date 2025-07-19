import random
import time

from dumbdisplay.core import *
from dumbdisplay.ddlayer import DDLayer, DD_RGB_COLOR
from dumbdisplay.ddlayer_graphical import DDLayerGraphical
from dumbdisplay.ddlayer_lcd import DDLayerLcd
from dumbdisplay.ddlayer_7segrow import DDLayer7SegmentRow


THICKER_LINE_SHADE = 223  # 0 to disable; other values can be 191 / 255


class MnistApp():
  def __init__(self, dd: DumbDisplay, inference_func = None):
    self.dd = dd
    self.inference_func = inference_func
    self.draw_layer: DDLayerGraphical = None
    self.copy_layer: DDLayerGraphical = None
    self.clear_btn: DDLayerLcd = None
    self.center_btn: DDLayerLcd = None
    self.inference_btn: DDLayerLcd = None
    self.result_layer: DDLayer7SegmentRow = None
    self.auto_center: bool = False
    self.last_x: int = -1
    self.last_y: int = -1
    self.pixels = None  # pixels data (28x28)


  def run(self):
      while True:
        (connected, reconnecting) = self.dd.connectPassive()
        if connected:
          if self.draw_layer is None:
            self.initializeDD()
          elif reconnecting:
            self.dd.masterReset()
            self.draw_layer = None
          else:
            self.updateDD()
        elif reconnecting:
          self.dd.masterReset()
          self.draw_layer = None

  def initializeDD(self):
    self.draw_layer = DDLayerGraphical(self.dd, 28, 28)
    self.draw_layer.border(1, "lightgray", "round", 0.5)
    self.draw_layer.enableFeedback("fs:drag", self._handleDrawLayerFeedback)

    self.copy_layer = DDLayerGraphical(self.dd, 28, 28)
    self.copy_layer.border(2, "blue", "round", 1)

    self.clear_btn = DDLayerLcd(self.dd, 7, 1)
    self.clear_btn.backgroundColor("lightgreen")
    self.clear_btn.pixelColor("darkblue")
    self.clear_btn.writeCenteredLine("clear")
    self.clear_btn.border(2, "darkgreen", "raised")
    self.clear_btn.enableFeedback("f", lambda *args: self._resetPixels())

    self.center_btn = DDLayerLcd(self.dd, 8, 1)
    self.center_btn.writeCenteredLine("center")
    self.center_btn.enableFeedback("fl", lambda *args: self._toggleAutoCenter())

    self.inference_btn = DDLayerLcd(self.dd, 3, 3)
    self.inference_btn.pixelColor("darkblue")
    self.inference_btn.writeCenteredLine(">>>", 1)
    self.inference_btn.border(2, "gray", "raised")
    self.inference_btn.enableFeedback("f", self._handleInferenceBtnFeedback)

    self.result_layer = DDLayer7SegmentRow(self.dd)
    self.result_layer.border(10, "blue", "round", 5)
    self.result_layer.segmentColor("darkblue")

    AutoPin('V',
      AutoPin('H', self.clear_btn, self.center_btn),
      self.draw_layer,
      AutoPin('H', self.copy_layer, self.inference_btn, self.result_layer),
    ).pin(self.dd)

    self.auto_center = False
    self._toggleAutoCenter()
    self._resetPixels()

  def updateDD(self):
    self.dd.timeslice()

  def _handleDrawLayerFeedback(self, layer: DDLayer, type: str, x: int, y: int):
    if x == -1:
      self.last_x = -1
      self.last_y = -1
    else:
      update = True
      if self.last_x == -1:
        self._drawPixel(x, y)
      else:
        if self.last_x != x or self.last_y != y:
          update = self._drawLine(self.last_x, self.last_y, x, y)
      if update:
        self.last_x = x
        self.last_y = y

  def _handleInferenceBtnFeedback(self, *args):
    self.draw_layer.disabled(True)
    if self.auto_center:
      self._autoCenterPixels(update_draw_layer = False)
    try:
      self.dd.log("<<< ...")
      start_time = time.time()
      if self.inference_func is not None:
        inference_data  = self._pixelsToInferenceData()
        best = self.inference_func(inference_data)
      else:
        best = random.randint(0, 10)
      taken_time = time.time() - start_time
      self.dd.log(f"... >>> in {taken_time:0.2f}s ==> [{best}]")
      self.result_layer.showDigit(best)
      self._drawPixelsTo(self.copy_layer)
      self._resetPixels()
    except Exception as e:
      self.dd.log(f"Error during inference: {e}", is_error=True)
    finally:
      self.draw_layer.disabled(False)

  def _toggleAutoCenter(self):
    self.auto_center = not self.auto_center
    if self.auto_center:
      self.center_btn.pixelColor("darkblue")
      self.center_btn.border(2, "gray", "flat")
    else:
      self.center_btn.pixelColor("gray")
      self.center_btn.border(2, "gray", "hair")


  def  _renderPixel(self, x: int, y: int, shade: int):
    if self.pixels[x][y] < shade:
      color = DD_RGB_COLOR(shade, shade, shade)
      self.draw_layer.drawPixel(x, y, color)
      self.pixels[x][y] = shade

  def _drawPixel(self, x: int, y: int):
    if THICKER_LINE_SHADE > 0:
      if x > 0:
        self._renderPixel(x - 1, y, THICKER_LINE_SHADE)
      if x < 27:
        self._renderPixel(x + 1, y, THICKER_LINE_SHADE)
      if y > 0:
        self._renderPixel(x, y - 1, THICKER_LINE_SHADE)
      if y < 27:
        self._renderPixel(x, y + 1, THICKER_LINE_SHADE)
    self._renderPixel(x, y, 255)

  def _drawLine(self, x1: int, y1: int, x2: int, y2: int) -> bool:
    delt_x = x2 - x1
    delt_y = y2 - y1
    if abs(delt_x) > abs(delt_y):
      steps = abs(delt_x)
      if steps == 0:
        return False  # nothing to draw
      inc_x = -1 if delt_x < 0 else 1
      inc_y = int(float(delt_y) / float(steps))
    else:
      steps = abs(delt_y)
      if steps == 0:
        return False  # nothing to draw
      inc_y = -1 if delt_y < 0 else 1
      inc_x = int(float(delt_x) / float(steps))
    x = float(x1)
    y = float(y1)
    self.dd.recordLayerCommands()
    for i in range(0, steps):
      self._drawPixel(round(x), round(y))
      x += inc_x
      y += inc_y
    self.dd.playbackLayerCommands()
    return True

  def _resetPixels(self):
    self.last_x = -1
    self.last_y = -1
    self.draw_layer.clear()
    self.pixels = [[0 for _ in range(28)] for _ in range(28)]

  def _drawPixelsTo(self, target_layer: DDLayerGraphical):
    self.dd.recordLayerCommands()
    target_layer.clear()
    for x in range(0, 28):
      for y in range(0, 28):
        shade = self.pixels[x][y]
        if shade != 0:
          target_layer.drawPixel(x, y, DD_RGB_COLOR(shade, shade, shade))
    self.dd.playbackLayerCommands()

  def _autoCenterPixels(self, update_draw_layer: bool = True):
    min_x = 27
    max_x = 0
    min_y = 27
    max_y = 0
    for x in range(0, 28):
      for y in range(0, 28):
        if self.pixels[x][y] != 0:
          if x < min_x:
            min_x = x
          if x > max_x:
            max_x = x
          if y < min_y:
            min_y = y
          if y > max_y:
            max_y = y
    x_delta = int((((27 - max_x) + min_x) / 2) - min_x)
    y_delta = int((((27 - max_y) + min_y) / 2) - min_y)
    if x_delta != 0 or y_delta != 0:
      new_pixels = [[0 for _ in range(28)] for _ in range(28)]
      for x in range(0, 28):
        for y in range(0, 28):
          new_x = x - x_delta
          new_y = y - y_delta
          pixel = 0
          if new_x >= 0 and new_x <= 27 and new_y >= 0 and new_y <= 27:
            pixel = self.pixels[new_x][new_y]
          new_pixels[x][y] = pixel
      self.pixels = new_pixels
      if update_draw_layer:
        self._drawPixelsTo(self.draw_layer)

  def _pixelsToInferenceData(self) -> list[float]:
    data = []
    for y in range(0, 28):
      for x in range(0, 28):
        shade = self.pixels[x][y]
        data.append(shade / 255.0)
    return data

