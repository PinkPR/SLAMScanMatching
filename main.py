#! /usr/bin/python -i

import socket, sys, pygame, math, operator
import Screen
import Ransac
import Server
import Serializer
import OptionParser
import Trigo
import Map
from threading import *

GAP       = 10.0
PI        = math.pi

size      = (width, height) = (500, 500)
screen    = Screen.Screen(800, 800, 300, 300)
options   = OptionParser.OptionParser(sys.argv)
mmap      = Map.Map(300, 300, 5)
pos       = [0, 0]
theta     = -PI / 2
plist     = []

def radmod(angle):
  return math.fmod(2 * PI + math.fmod(angle, 2 * PI), 2 * PI)

def angToCart(radius, angle):
  return (pos[0] + radius * math.cos(angle),
          pos[1] + radius * math.sin(angle))

def cartToReal(x, y):
  return (width / 2 + x,
          height / 2 - y)

def drawPointList(screen, points, color):
  for i in range(0, len(points)):
    screen.drawRect(points[i][0], points[i][1], 4, 4, color, 0)

def applyRansac(screen, points, color, error):
  col = (255, 0 , 0)
  i = 0
  len1 = len(points) + 1
  while len(points) <> len1:
    len1 = len(points)
    ransacPoints = Ransac.compute(points, error)
    print '|Ransac points| = ' + str(len(ransacPoints))
    if len(ransacPoints) <> 0:
      screen.drawMaxLine(ransacPoints, col)
      points = [x for x in points if x not in ransacPoints]
      i += 1
      col = (col[0], col[1] + 10, col[2])
  return points

def recTranslation(conn):
  for i in range(2):
    rec = conn.recv(1024)
    if not rec:
      return
    pos[i] = pos[i] + float(rec)

def recRotation(conn):
  rec = conn.recv(1024)
  if not rec:
    return
  theta = radmod(theta + float(rec))

def recMeasurement(conn):
  print "Measurement"
  radius = 0
  angle  = 0
  for i in range(2):
    rec = conn.recv(1024)
    print("recorded : " + rec)
    if not rec:
      break
    if i == 0:
      radius = float(rec)
      if radius >= 90:
        return
    if i == 1:
      angle = float(rec) + theta
  print ("radius : " + str(radius))
  print ("angle  : " + str(angle))
  coord = map(operator.add, pos, angToCart(radius, angle))
  plist.append(coord)
  mmap.setCellRaw(coord, 1)
  mmap.draw(screen)

def addMovementToCoord(coord, position):
  return (coord[0] + position[0], coord[1] + position[1])

handlers  = { "T" : recTranslation, "R" : recRotation, "M" : recMeasurement }

def handleCommand(conn):
  command = ""
  lst     = ["T", "R", "M"]

  while not command in lst:
    command = conn.recv(1024)
    if not command:
      return False

  handlers[command[0]](conn)
  return True

HOST = ''
PORT = 8888

if options.load:
  plist = Serializer.load(options.filename)
  for i in range(len(plist)):
    mmap.setCellRaw(plist[i], 1)
  mmap.draw(screen)
  #plist = Trigo.computeRealPositions(plist, 10.0)
  #screen.drawAxis(Screen.PINK, Screen.PINK)
  #screen.drawXScale(Screen.WHITE, 50)
  #screen.drawYScale(Screen.WHITE, 50)
  #drawPointList(screen, Trigo.computeRealPositions(plist, 10.0), Screen.LIGHTBLUE)
  #Ransac.cleanIsolatedPoints(plist)
  #drawPointList(screen, plist, Screen.BLUE)
  #plist = applyRansac(screen, plist, Screen.GREEN, 5.0)
  #drawPointList(screen, plist, Screen.BLUE)
  screen.save('result.bmp')
  print 'Image Saved !'
  sys.exit()

def thrd(conn):

  while handleCommand(conn):
    continue

    #coord = angToCart(float(data1), float(data2))
    #plist.append(coord)
    #mmap.setCellRaw(coord, 1)
    #mmap.draw(screen)

  print("LOCAL MAPPING DONE")
  while True:
    continue
  if options.save:
    Serializer.save(options.filename, plist)

  conn.close()
  return

server = Server.Server(HOST, PORT)
server.listen(1)
connaddr = server.accept()

mmap.draw(screen)
server.threadFunc(thrd, (connaddr[0],))

#while True:
  #screen.draw()
