import Screen

class Map:
  def __init__(self, X, Y, size, robot):
    self.X          = X
    self.Y          = Y
    self.cell_size  = size
    self.matrix     = [ [ [0.5, 0, 0, 0] for i in range(X / size) ] for j in range(Y / size)]
    self.lmatrix    = [ [ 0 for i in range(X / size) ] for j in range(Y / size)]
    self.robot      = robot

  def getRobot(self):
    return self.robot

  def setRobot(self, robot):
    self.robot = robot

  def absoluteToReal(self, (x, y)):
    return (x * size, y * size)

  def realToAbsolute(self, (x, y)):
    xx = (x + self.X / 2) / self.cell_size
    yy = self.Y / self.cell_size - (y + self.cell_size + self.Y / 2) / self.cell_size
    return (int(xx), int(yy))

  def getVectorFromReal(self, (x1, y1), (x2, y2)):
    absolute1 = self.realToAbsolute((x1, y1))
    absolute2 = self.realToAbsolute((x2, y2))
    return (absolute2[0] - absolute1[0], absolute2[1] - absolute1[1])

  def getCell(self, (x, y)):
    return self.matrix[int(x)][int(y)][0]

  def getCellRaw(self, (x, y)):
    x = (x + self.X / 2) / self.cell_size
    y = self.Y / self.cell_size - (y + self.cell_size + self.Y / 2) / self.cell_size
    return self.matrix[x][y]

  def getCellColor(self, (x, y)):
    return self.matrix[int(x)][int(y)][1:]

  def getLCell(self, (x, y)):
    return self.lmatrix[x][y]

  def getLCellRaw(self, (x, y)):
    x = (x + self.X / 2) / self.cell_size
    y = self.Y / self.cell_size - (y + self.cell_size + self.Y / 2) / self.cell_size
    return self.lmatrix[x][y]

  def setCell(self, (x, y), val):
    self.matrix[x][y][0] = val

  def setCellRaw(self, (x, y), val):
    x = (x + self.X / 2) / self.cell_size
    y = self.Y / self.cell_size - (y + self.cell_size + self.Y / 2) / self.cell_size
    self.setCell((int(x), int(y)), val)

  def setLCell(self, (x, y), val):
    self.lmatrix[x][y] = val

  def setLCellRaw(self, (x, y), val):
    x = (x + self.X / 2) / self.cell_size
    y = self.Y / self.cell_size - (y + self.cell_size + self.Y / 2) / self.cell_size
    self.lmatrix[x][y] = val

  def setCellColor(self, (x, y), col):
    self.matrix[x][y][1:] = col

  def setCellColorRaw(self, (x, y), col):
    x = (x + self.X / 2) / self.cell_size
    y = self.Y / self.cell_size - (y + self.cell_size + self.Y / 2) / self.cell_size
    self.setCellColor((int(x), int(y)), col)

  def addListRaw(self, plist, val, color=[0, 0, 0]):
    for i in range(len(plist)):
      self.setCellRaw(plist[i], val)
      self.setCellColorRaw(plist[i], color)

  def mulCell(self, (x, y), val):
    self.setCell((x, y), self.getCell((x, y)) * val)

  def divCell(self, (x, y), val):
    self.setCell((x, y), self.getCell((x, y)) / val)

  def addCell(self, (x, y), val):
    self.setCell((x, y), self.getCell((x, y)) + val)

  def subCell(self, (x, y), val):
    self.setCell((x, y), self.getCell((x, y)) - val)

  def drawScale(self, screen):
    screen.drawXScale(Screen.GREY, self.cell_size)
    screen.drawYScale(Screen.GREY, self.cell_size)
    screen.drawAxis(Screen.WHITE, Screen.WHITE)

  def drawMap(self, screen):
    for i in range(0, self.X / self.cell_size):
      for j in range(0, self.Y / self.cell_size):
        color = self.getCellColor((i, j))
        if color == [0, 0, 0]:
          col   = 255 * self.getCell((i, j))
          color = (col, col, col)

        screen.drawRectangleAbsolute(i * self.cell_size + 1,
                                     j * self.cell_size + 1,
                                     self.cell_size - 2,
                                     self.cell_size - 2,
                                     color)

  def drawRobot(self, screen):
    coord = self.realToAbsolute(self.robot.getPos())
    screen.drawRectangleAbsolute(coord[0] * self.cell_size + 1,
                                 coord[1] * self.cell_size + 1,
                                 self.cell_size - 2,
                                 self.cell_size - 2,
                                 (0, 255, 0))

  def draw(self, screen):
    self.drawMap(screen)
    self.drawRobot(screen)
    self.drawScale(screen)
    screen.draw()
