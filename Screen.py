import pygame
import Ransac
import math

RED       = pygame.Color(0xFF,    0,      0)
BLUE      = pygame.Color(0,       0,      0xFF)
LIGHTBLUE = pygame.Color(0,       0xFF,   0xFF)
GREEN     = pygame.Color(0,       0xFF,   0)
YELLOW    = pygame.Color(0xFF,    0xFF,   0)
PINK      = pygame.Color(0xFF,    0x99,   0xFF)
WHITE     = pygame.Color(0xFF,    0xFF,   0xFF)
GREY      = pygame.Color(0x10,    0x10,   0x10)
class Screen:
  def __init__(self, width, height, rWidth, rHeight):
    """
    Constructor for Screen.

    @type   width   :   int
    @param  width   :   widht of the window to be created
    @type   height  :   int
    @param  height  :   height of the window to be created
    @type   rWidth  :   int
    @param  rWidth  :   width of the real scene to be represented
    @type   rHeight :   int
    @param  rHeight :   height of the real scene to be represented
    """
    self.width    = width
    self.height   = height
    self.rWidth   = rWidth
    self.rHeight  = rHeight
    self.size     = (width, height)
    self.surface  = pygame.Surface(self.size)
    pygame.init()
    self.screen   = pygame.display.set_mode(self.size)

  def CartToReal(self, x, y):
    """
    Converts a cartesian coordinate in the space of rWidth/rHeight in
    cartesian coordinates in the width/height space.
    !!! WARNING !!! : x and y are supposed to be relative to the center of
    the screen. That means that x and y may be negative. The returned
    coordinates are absolute to the top left corner of the screen.

    @type     x   :   float
    @param    x   :   x coordinate of the point
    @type     y   :   float
    @param    y   :   y coordinate of the point

    @rtype        :   (int, int)
    @return       :   the transposed coordinates in the width/height space
    """
    x   += self.rWidth / 2
    y   += self.rHeight / 2
    xdiv = float(x) / float(self.rWidth)
    ydiv = float(y) / float(self.rHeight)
    xx   = int(xdiv * float(self.width))
    yy   = self.height - int(ydiv * float(self.height))
    return (xx, yy)

  def computeDistance(self, (x1, y1), (x2, y2)):
    """
    Computes the distance between 2 points.

    @type     x1  :   float
    @param    x1  :   x coordinate of point 1
    @type     y1  :   float
    @param    y1  :   y coordinate of point 1
    @type     x2  :   float
    @param    x2  :   x coordinate of point 2
    @type     y2  :   float
    @param    y2  :   y coordinate of point 2

    @rtype        :   float
    @return       :   the distance between the 2 points passed as arguments
    """
    return math.sqrt((x1 - x2) * (x1 - x2) +
                     (y1 - y2) * (y1 - y2))

  def drawLine(self, (x1, y1), (x2, y2), color):
    """
    Draw an antialiased line from (x1, y1) to (x2, y2) of the given color
    !!! WARNING !!! (x1, y1) and (x2, y2) are relative coordinates

    @type     x1  :   float
    @param    x1  :   x coordinate of point 1
    @type     y1  :   float
    @param    y1  :   y coordinate of point 1
    @type     x2  :   float
    @param    x2  :   x coordinate of point 2
    @type     y2  :   float
    @param    y2  :   y coordinate of point 2
    """
    pygame.draw.aaline(self.surface,
                       color,
                       self.CartToReal(x1, y1),
                       self.CartToReal(x2, y2),
                       1)

  def drawRectangle(self, x, y, w, h, color):
    (xx, yy) = self.CartToReal(x, y)
    pygame.draw.rect(self.surface,
                     color,
                     pygame.Rect(xx, yy, w, h),
                     0)

  def drawRectangleAbsolute(self, x, y, w, h, color):
    xx = self.width  * x / self.rWidth
    yy = self.height * y / self.rHeight

    ww = self.width  * w / self.rWidth
    hh = self.height * h / self.rHeight

    pygame.draw.rect(self.surface,
                     color,
                     pygame.Rect(xx, yy, ww, hh),
                     0)

  def drawRect(self, x, y, w, h, color, contour=0):
    """
    Draw a rectangle centered at (x, y) and which is (w, h) pixels high and
    thick.
    !!! WARNING !!! (x, y) are relative coordinates

    @type     x       :   float
    @param    x       :   x coordinate of the rectangle center
    @type     y       :   float
    @param    y       :   y coordinate of the rectangle center
    @type     w       :   int
    @param    w       :   width of the rectangle (in pixels)
    @type     h       :   int
    @param    h       :   height of the rectangle (in pixels)
    @type     color   :   (int, int, int)
    @param    color   :   color of the rectangle. Colors are 24 bits RGB
    @type     contour :   int
    @param    contour :   size of the rectangle contour (in pixels).
                          if contour == 0, the rectangle is fully drawn
    """
    (xx, yy) = self.CartToReal(x, y)
    xx  -= w / 2
    yy  -= h / 2

    pygame.draw.rect(self.surface,
                     color,
                     pygame.Rect(xx, yy, w, h),
                     contour)

  def drawAxis(self, xcolor, ycolor):
    """
    Draw the x and y axis with the given colors

    @type     xcolor  :   (int, int, int)
    @param    xcolor  :   color of the x axis. Colors are 24 bits RGB
    @type     ycolor  :   (int, int, int)
    @param    ycolor  :   color of the y axis. Colors are 24 bits RGB
    """
    self.drawLine((self.rWidth / 2, 0), (-self.rWidth / 2, 0), xcolor)
    self.drawLine((0, self.rHeight / 2), (0, -self.rHeight / 2), ycolor)

  def drawXScale(self, color, gap):
    i = gap
    while i < self.rWidth / 2:
      self.drawLine((i, self.rHeight / 2), (i, -self.rHeight / 2), color)
      self.drawLine((-i, self.rHeight / 2), (-i, -self.rHeight / 2), color)
      i = i + gap

  def drawYScale(self, color, gap):
    i = gap
    while i < self.rHeight / 2:
      self.drawLine((self.rWidth / 2, i), (-self.rHeight / 2, i), color)
      self.drawLine((self.rWidth / 2, -i), (-self.rHeight / 2, -i), color)
      i = i + gap

  def drawMaxLine(self, points, color):
    """
    Look for the 2 most far points in the list and draws a line between them.

    @type     points  :   [(float, float)]
    @param    points  :   list of points to be managed
    @type     color   :   (int, int, int)
    @param    color   :   the color of the line. Colors are 24 bits RGB
    """
    print 'In drawMaxLine'
    print 'card(points) = ' + str(len(points))
    point1 = (0, 0)
    point2 = (0, 0)
    dist   = 0
    for i in range(0, len(points) - 1):
      for j in range(i + 1, len(points)):
        distance = self.computeDistance(points[i], points[j])
        if distance > dist:
          point1 = points[i]
          point2 = points[j]
          dist = distance
    self.drawLine(point1, point2, color)

  def draw(self):
    """
    Draw the scene
    """
    self.screen.blit(self.surface, (0, 0))
    pygame.display.flip()

  def save(self, name):
    """
    Save an image of the scene.

    @type     name  :   string
    @param    name  :   name of the image file
    """
    pygame.image.save(self.surface, name)
