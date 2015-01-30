import copy
import Map
import Trigo

CELL_FREE = 1.0
CELL_OCC  = 0.0
CELL_INIT = 0.5

def sumPolarCoordinates(p1, p2):
  return Trigo.angToCart((p1[0] + p2[0], p1[1] + p2[1]))

def compute_Y(x, (a, b)):
  return a * x + b

def cross_square(xmin, xmax, ymin, ymax, (a, b)):
  for i in range(0, 10):
    y = compute_Y(xmin + i * (xmax - xmin) / 10.0, (a, b))

    if (y < ymax or y > ymin):
      return True

  return False

def getPerceptualField((r, theta)):
  perceptual_field = []

  for i in range(0, int(r)):
    perceptual_field.append((i, theta))

  return perceptual_field

def occupancy_grid_mapping(grid_map, pos, measurements, screen):
  print "GRID MAPPING"
  perceptual_field = []

  for i in range(len(measurements)):
    perceptual_field = perceptual_field + getPerceptualField(measurements[i])

  for i in range(len(perceptual_field)):
    grid_map.setCellRaw(sumPolarCoordinates(pos, perceptual_field[i]), CELL_FREE)
    grid_map.draw(screen)

  for i in range(len(measurements)):
    grid_map.setCellRaw(sumPolarCoordinates(pos, measurements[i]), CELL_OCC)
    grid_map.draw(screen)
