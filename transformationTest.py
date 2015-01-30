import Screen
import Serializer
from math import *

screen = Screen.Screen(800, 800, 300, 300)
screen.drawAxis(Screen.WHITE, Screen.WHITE)

def drawPoint(point, color):
  screen.drawRect(point[0], point[1], 4, 4, color, 0)
  screen.draw()

def drawPointList(points, color):
  for i in range(len(points)):
    drawPoint(points[i], color)

def applyQ(point, q):
  return (q[0] + cos(q[2]) * point[0] - sin(q[2]) * point[1],
          q[1] + sin(q[2]) * point[0] + cos(q[2]) * point[1])

def applyQList(points, q):
  ret = []

  for i in range(len(points)):
    ret.append(applyQ(points[i], q))

  return ret

set1 = Serializer.load("pointset1")
set2 = Serializer.load("pointset2")

drawPointList(applyQList(applyQList(set2, (0, 0, pi / 2)), (0, 0, -pi / 2)), Screen.GREEN)
drawPointList(set1, Screen.BLUE)
