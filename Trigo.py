import math

PI = math.pi

def cartToAng((x, y)):
  """
  Return the polar coordinates corresponding to the cartesian coordinates
  (x, y)

  @type   x   :   float
  @param  x   :   x value of the cartesian coordinate
  @type   y   :   float
  @param  y   :   x value of the cartesian coordinate
  @rtype      :   (float, float)
  @return     :   the corresponding polar coordinates
  """
  radius  = math.hypot(x, y)
  angle   = 2.0 * math.atan2(y, x + math.hypot(x, y))
  return (radius, angle)

def angToCart((radius, angle)):
  """
  Return the cartesian coordinates corresponding to the polar coordinates
  (radius, angle)

  @type   radius  :   float
  @param  radius  :   distance from (0, 0) of the point
  @type   angle   :   float
  @param  angle   :   oriented angle ((0, 0), (x, y)) with (x, y) the cartesian
                      coordinates of the point. angle must be in radians
  @rtype          :   (float, float)
  @return         :   the corresponding cartesian coordinates
  """
  return (radius * math.cos(angle),
          radius * math.sin(angle))

def getRealPos((x, y), gap):
  """
  I noticed that the sonar measurements could be corrupted because of the
  position of the sonar on the robot's head. I mean, the sonar is placed on
  the robot's left ear, not in the center of the head as it must be. The
  goal of this function is to fix this value in order to simulate a head
  centered sonar.

  @type   x       :   float
  @param  x       :   x value of the cartesian coordinate
  @type   y       :   float
  @param  y       :   y value of the cartesian coordinate
  @type   gap     :   float
  @param  gap     :   distance between the sonar and the head center
  @rtype          :   (float, float)
  @return         :   the re-computed position of the point, in cartesian
                      coordinate
  """
  polar   = cartToAng((x, y))
  radius  = math.hypot(polar[0], gap)
  theta   = polar[1] + math.acos(polar[0] / radius)
  return angToCart((radius, theta))

def computeRealPositions(points, gap):
  """
  Fix the non-head-centered-sonar problem for every point in points

  @type   points  :   [(float, float)]
  @param  points  :   list of points to be re-computed, in cartesian
                      coordinates
  @type   gap     :   float
  @param  gap     :   distance between the sonar and the head center
  @rtype          :   [(float, float)]
  @return         :   the re-computed points list
  """
  real = []
  for i in range(0, len(points)):
    real.append(getRealPos(points[i], gap))
  return real
