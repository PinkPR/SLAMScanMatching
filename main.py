#! /usr/bin/python

import Screen
import Map
import Server
import Trigo
import Robot
import STCExplorer
import sys

points = []

def handleRequest(grid_map, robot, request):
  if request[0] == 'M':
    point = robot.recMeasurement()
    if (not point[0] == 0):
      points.append(point)
      grid_map.setCellRaw(Trigo.angToCart(point), 0.0)

screen      = Screen.Screen(800, 800, 300, 300)
server      = Server.Server('', 8888)
server.listen(1)
conn, addr  = server.accept()
robot       = Robot.Robot(conn, [0, 0])
grid_map    = Map.Map(300, 300, 20, robot)

grid_map.draw(screen)

STCExplorer.STC(grid_map, None, robot, screen)

while True:
  grid_map.draw(screen)

request = robot.rec(8)

while request:
  handleRequest(grid_map, robot, request)
  request = robot.rec(8)
  grid_map.draw(screen)

while True:
  grid_map.draw(screen)
