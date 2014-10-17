class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def draw(screen, color):
    screen.drawRect(x, y, 5, 5, color)

class Line:
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2

  def draw(screen, color):
    screen.drawLine(self.p1, self.p2, color)

class Rectangle:
  def __init__(self, x, y, w, h):
    self.x = x
    self.y = y
    self.w = w
    self.h = h

  def draw(screen, color):
    screen.drawRectangle(x, y, w, h, color)
