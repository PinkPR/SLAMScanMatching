import math
import random
import copy
import Line

MAX_DIST_ISOLATED = 10.0
MAX_DIST_LINE     = 10.0

def cleanIsolatedPoints(points):
  """
  Remove the points which are at least MAX_DIST_ISOLATED far from the others.

  @type     points  :   [(int, int)]
  @param    points  :   the list of points to be cleaned
  """
  i = 0
  j = 0
  b = False

  while i < len(points):
    j = 0
    b = False
    while j < len(points):
      if j == i:
        j = j + 1
        continue
      if getDistancePointPoint(points[i], points[j]) <= MAX_DIST_ISOLATED:
        b = True
        break
      j = j + 1
    if not b:
      points.remove(points[i])
      i = i - 1
    i = i + 1

def getNumberOfNeighbours(points, n, dist):
  """
  Return the number of points which are at most dist far from the others in
  the list.

  @type     points  :   [(float, float)]
  @param    points  :   list of points to be considered
  @type     n       :   int
  @param    n       :   index of the point in the list
  @type     dist    :   float
  @param    dist    :   maximum distance to consider two points as neighbours

  @rtype            :   int
  @return           :   number of neighbours
  """
  count = 0
  for i in range(0, len(points)):
    if i == n:
      continue
    if getDistancePointPoint(points[i], points[n]) <= dist:
      count = count + 1
  return count

def findLineEq((x1, y1), (x2, y2)):
  """
  Compute a line equation of the form y = ax + b according to two points
  on this line.

  @type     x1    :   float
  @param    x1    :   x coordinate of point 1
  @type     y1    :   float
  @param    y1    :   y coordinate of point 1
  @type     x2    :   float
  @param    x2    :   x coordinate of point 2
  @type     y2    :   float
  @param    y2    :   y coordinate of point 2

  @rtype          :   (float, float)
  @return         :   the slope and the constant a and b
  """
  if (x1 == x2):
    return (0.0, 0,0)
  a = float(y1 - y2) / float(x1 - x2)
  b = float(y1) - a * float(x1)
  return (a, b)

def findDistanceLinePoint((a, b), (x, y)):
  """
  Compute the distance between a line and a point.

  @type     a   :   float
  @param    a   :   slope of the line
  @type     b   :   float
  @param    b   :   constant of the line equation
  @type     x   :   float
  @param    x   :   x coordinate of the point
  @type     y   :   float
  @param    y   :   y coordinate of the point

  @rtype        :   float
  @return       :   the distance between the point and the line
  """
  return abs(a * x + -1.0 * y + b) / math.sqrt(a * a + 1.0)

def generateRandomPoints(maxx, maxy, n):
  """
  Generate a list of n random points in the range ([-maxx / 2, maxx / 2], [-maxy / 2, maxy / 2]).

  @type     maxx  :   int
  @param    maxx  :   range to generate the x coordinates
  @type     maxy  :   int
  @param    maxy  :   range to generate the y coordinates
  @type     n     :   int
  @param    n     :   number of points to generate

  @rtype          :   [(int, int)]
  @return         :   the list of the n generated points
  """
  l = []
  for i in range(0, n):
    random.seed()
    l.append((random.randint(0, maxx) - maxx / 2,
              random.randint(0, maxy) - maxy / 2))
  return l

def getDistancePointPoint((x1, y1), (x2, y2)):
  """
  Compute the distance between two points.

  @type     x1  :   float
  @param    x1  :   x coordinate of point 1
  @type     y1  :   float
  @param    y1  :   y coordinate of point 1
  @type     x2  :   float
  @param    x2  :   x coordinate of point 2
  @type     y2  :   float
  @param    y2  :   y coordinate of point 2

  @rtype        :   float
  @return       :   the distance between the two points
  """
  return math.hypot(x2 - x1, y2 - y1)

def isAcceptable(points, index, margin):
  """
  Return True if the point at point[index] has at least one point close of it
  (margin far).

  @type     points  :   [(int, int)]
  @param    points  :   list of points to be considered.
  @type     index   :   int
  @param    index   :   index of the point in the list to determine as acceptable
  @type     margin  :   float
  @param    margin  :   maximum distance between two points to consider one
  point as acceptable

  @rtype            :   bool
  @return           :   True if point is acceptable, False otherwise
  """
  for i in range(0, len(points)):
    if i == index:
      continue
    if (getDistancePointPoint(points[i], points[index]) <= margin):
      return True
  return False

def cleanDaShit(points):
  k = 0
  #cleanIsolatedPoints(points)

  while k < len(points):
    res = getNumberOfNeighbours(points, k, 30.0)
    if res < 2:
      points.remove(points[k])
      continue
    k = k + 1

def compute(points, error):
  """
  Compute the best fit line for the RANSAC algorithm.

  @type     points  :   [(float, float)]
  @param    points  :   list of points to be considered in the algorithm
  @type     error   :   float
  @param    error   :   maximum distance between points and lines to be accepted
  by the algorithm

  @rtype            :   [(float, float)]
  @return           :   the list of the points computed to be part of the best fit line
  """
  master       = Line.Line(0, 0)
  challenger   = Line.Line(0, 0)
  tup          = (0, 0)
  length       = 0

  for i in range(0, len(points)):
    for j in range(0, len(points)):
      if j == i:
        continue
      tup = findLineEq(points[i], points[j])
      challenger = Line.Line(tup[0], tup[1])
      challenger.points = []

      # Finding points that statisfy the error condition
      for k in range(0, len(points)):
        if findDistanceLinePoint((tup[0], tup[1]), points[k]) <= error:
          challenger.appendPoint((points[k]))

      cleanDaShit(challenger.points)

      if len(challenger.points) > len(master.points) and len(challenger.points) > 4:
        master = copy.deepcopy(challenger)

  return master.points
