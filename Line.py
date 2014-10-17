import Ransac

class Line:
  def __init__(self, a, b):
    """
    Constructor for Line. The line equation form is y = ax + b. The points
    attribute is a list of points which are close to this line.

    @type     a   :   float
    @param    a   :   slope of the line
    @type     b   :   float
    @param    b   :   constant
    """
    self.a      = a
    self.b      = b
    self.points = []

  def appendPoint(self, (x, y)):
    """
    Append a point to the points list.

    @type     x   :   int
    @param    x   :   x coordinate of the point to be added
    @type     y   :   int
    @param    y   :   y coordinate of the point to be added
    """
    self.points.append((x, y))
