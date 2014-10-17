import math
from decimal import *
import numpy as np
import Ransac
import Trigo

L = 3
PI = math.pi

def dot((x1, y1), (x2, y2)):
  return x1 * x2 + y1 * y2

def vector((x1, y1), (x2, y2)):
  return (x2 - x1, y2 - y1)

def norma((x, y)):
  return math.hypot(x, y)

def radmod(angle):
  return math.fmod(2 * PI + math.fmod(angle, 2 * PI), 2 * PI)

def radmodDecimal(angle):
  return (Decimal(2 * PI) + (angle % Decimal(2 * PI))) % Decimal(2 * PI)

def isOnSegment(C, (A, B)):
  AC = vector(A, C)
  CB = vector(C, B)
  AB = vector(A, B)

  if (norma(AC) + norma(CB) == norma(AB)):
    return True
  else:
    return False

def getProjection((xa, ya), ((x1, y1), (x2, y2))):
  xu = x2 - x1
  yu = y2 - y1
  a, b = Ransac.findLineEq((x1, y1), (x2, y2))

  xh = (xa * xu - b * yu + ya * yu) / (xu + a * yu)
  yh = a * xh + b

  return (xh, yh)

def getMatchPointSegment((xa, ya), ((x1, y1), (x2, y2))):
  xh, yh = getProjection((xa, ya), ((x1, y1), (x2, y2)))

  if not isOnSegment((xh, yh), ((x1, y1), (x2, y2))):
    if norma(vector((xa, ya), (x1, y1))) < norma(vector((xa, ya), (x2, y2))):
      return (x1, y1)
    else:
      return (x2, y2)
  else:
    return (xh, yh)

def findMatchingPoint(point, ref):
  challenger  = getMatchPointSegment(point, (ref[0], ref[1]))
  dist        = norma(vector(point, challenger))

  for i in range(1, len(ref) - 1):
    tmp_challenger  = getMatchPointSegment(point, (ref[i], ref[i + 1]))
    tmp_dist        = norma(vector(point, tmp_challenger))

    if (tmp_dist < dist):
      challenger  = tmp_challenger
      dist        = tmp_dist

  return challenger

def matchPoints(ref, new, new2):
  result = []

  for i in range(len(new)):
    result.append((new2[i], findMatchingPoint(new[i], ref)))

  return result

def applyQ((xa, ya), (x, y, theta)):
  xa = xa + float(x)
  ya = ya + float(y)

  xa, ya = Trigo.cartToAng((xa, ya))
  ya     = radmod(ya + float(theta))

  return Trigo.angToCart((xa, ya))

def applyQList(points, (x, y, theta)):
  for i in range(len(points)):
    points[i] = applyQ(points[i], (x, y, theta))

def getA11(match):
  res = Decimal(0)
  k = Decimal(0)

  for i in range(len(match)):
    pix = Decimal(match[i][1][0])
    piy = Decimal(match[i][1][1])
    cix = Decimal(match[i][0][0])
    ciy = Decimal(match[i][0][1])
    ki  = pix ** 2 + piy ** 2 + L ** 2

    res = res + (1 - piy ** 2 / ki)

  return res

def getA12(match):
  res = Decimal(0)
  k = Decimal(0)

  for i in range(len(match)):
    pix = Decimal(match[i][1][0])
    piy = Decimal(match[i][1][1])
    cix = Decimal(match[i][0][0])
    ciy = Decimal(match[i][0][1])
    ki  = pix ** 2 + piy ** 2 + L ** 2

    res = res + (pix * piy / ki)

  return res

def getA13(match):
  res = Decimal(0)
  k = Decimal(0)

  for i in range(len(match)):
    pix = Decimal(match[i][1][0])
    piy = Decimal(match[i][1][1])
    cix = Decimal(match[i][0][0])
    ciy = Decimal(match[i][0][1])
    ki  = pix ** 2 + piy ** 2 + L ** 2

    res = res + (-ciy + (cix * pix + ciy * piy) * piy / ki)

  return res

def getA22(match):
  res = Decimal(0)
  k = Decimal(0)

  for i in range(len(match)):
    pix = Decimal(match[i][1][0])
    piy = Decimal(match[i][1][1])
    cix = Decimal(match[i][0][0])
    ciy = Decimal(match[i][0][1])
    ki  = pix ** 2 + piy ** 2 + L ** 2

    res = res + (1 - pix ** 2 / ki)

  return res

def getA23(match):
  res = Decimal(0)
  k = Decimal(0)

  for i in range(len(match)):
    pix = Decimal(match[i][1][0])
    piy = Decimal(match[i][1][1])
    cix = Decimal(match[i][0][0])
    ciy = Decimal(match[i][0][1])
    ki  = pix ** 2 + piy ** 2 + L ** 2

    res = res + (cix - (cix * pix + ciy * piy) * pix / ki)

  return res

def getA33(match):
  res = Decimal(0)
  k = Decimal(0)

  for i in range(len(match)):
    pix = Decimal(match[i][1][0])
    piy = Decimal(match[i][1][1])
    cix = Decimal(match[i][0][0])
    ciy = Decimal(match[i][0][1])
    ki  = pix ** 2 + piy ** 2 + L ** 2

    res = res + (cix ** 2 + ciy ** 2 - ((cix * pix + ciy * piy) ** 2) / ki)

  return res

def getB1(match):
  res = Decimal(0)
  k = Decimal(0)

  for i in range(len(match)):
    pix = Decimal(match[i][1][0])
    piy = Decimal(match[i][1][1])
    cix = Decimal(match[i][0][0])
    ciy = Decimal(match[i][0][1])
    ki  = pix ** 2 + piy ** 2 + L ** 2

    res = res + (cix - pix - (cix * piy - ciy * pix) * piy / ki)

  return res

def getB2(match):
  res = Decimal(0)
  k = Decimal(0)

  for i in range(len(match)):
    pix = Decimal(match[i][1][0])
    piy = Decimal(match[i][1][1])
    cix = Decimal(match[i][0][0])
    ciy = Decimal(match[i][0][1])
    ki  = pix ** 2 + piy ** 2 + L ** 2

    res = res + (ciy - piy - (cix * piy - ciy * pix) * pix / ki)

  return res

def getB3(match):
  res = Decimal(0)
  k = Decimal(0)

  for i in range(len(match)):
    pix = Decimal(match[i][1][0])
    piy = Decimal(match[i][1][1])
    cix = Decimal(match[i][0][0])
    ciy = Decimal(match[i][0][1])
    ki  = pix ** 2 + piy ** 2 + L ** 2

    res = res + (((cix * pix + cix * piy) / ki - 1) * (cix * piy - ciy * pix))

  return res

def getA(match):
  return np.array([[getA11(match), getA12(match), getA13(match)],
                   [getA12(match), getA22(match), getA23(match)],
                   [getA13(match), getA23(match), getA33(match)]])

def getB(match):
  return np.array([[getB1(match)],
                   [getB2(match)],
                   [getB3(match)]])

def floatMatrixToDecimal(mat):
  M = [[[Decimal(0), Decimal(0), Decimal(0)] for i in range(len(mat[0]))] for j in range(len(mat))]

  for i in range(len(mat)):
    for j in range(len(mat[0])):
      M[i][j] = Decimal(mat[i][j])

  return M

def getQmin(match):
  A = getA(match)
  B = getB(match)
  A = np.linalg.matrix_power(A, -1)
  A = -A
  A = floatMatrixToDecimal(A)

  return np.dot(A, B)

def runScanMatching(ref, new, q):
  match = []
  tmp   = []
  qmin  = (Decimal(q[0]), Decimal(q[1]), Decimal(q[2]))

  for i in range(100):
    tmp = list(new)
    applyQList(tmp, qmin)
    match = matchPoints(ref, tmp, new)
    qmin = getQmin(match)
    qmin[2] = radmodDecimal(qmin[2])
    print qmin

  return qmin
