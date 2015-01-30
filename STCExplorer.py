import math

import Map
import Robot
import Trigo

OLD_CELL = 1
NEW_CELL = 0

def getNextFreeCell(grid_map, current_cell):
  dirs = [[1, 0],
          [1, 1],
          [0, 1],
          [-1, 1],
          [-1, 0],
          [-1, -1],
          [0, -1],
          [1, -1]]

  for i in range(len(dirs)):
    target = [dirs[i][0] * grid_map.cell_size + current_cell[0],
              dirs[i][1] * grid_map.cell_size + current_cell[1]]

  if (grid_map.getLCellRaw(target) == NEW_CELL or grid_map.getCellRaw(target) == 0.0):
    return target, dirs[i]

  return None, None

def computeTranslation(grid_map, current_cell, target):
  vector = grid_map.getVectorFromReal(current_cell, target)

  return (math.hypot(vector[0], vector[1]), 0)

#def computeRotation(vector1, vector2):
  #return math.acos(vector1[0] * vector2[0] + vector1[1] + vector2[1])

def computeRotation(vector1, vector2):
  return math.atan2(vector1[1], vector1[0]) - math.atan2(vector2[1], vector2[0])

def handleRequest(grid_map, robot, request):
  if request[0] == 'M':
    point = robot.recMeasurement()
    if (not point[0] == 0):
      #points.append(point)
      grid_map.setCellRaw(Trigo.angToCart(point), 0.0)

def STC(grid_map, prev_cell, robot, screen):
  request = robot.rec(8)

  while request:
    handleRequest(grid_map, robot, request)
    request = robot.rec(8)
    grid_map.draw(screen)

  current_cell = robot.getPos()
  grid_map.setLCellRaw(current_cell, OLD_CELL)
  next_cell, direction = getNextFreeCell(grid_map, current_cell)

  while next_cell:
    # Move to target
    print "Chosen direction : " + str(direction)
    robot.sendRotation(computeRotation(direction, robot.orient))
    robot.sendTranslation(computeTranslation(grid_map, robot.pos, next_cell))

    robot.setOrient(direction)
    robot.setPos(next_cell)
    next_cell = None
    #STC(grid_map, current_cell, robot, screen)
