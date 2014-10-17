import Screen

class Map:
  def __init__(self, X, Y, size):
    self.X          = X
    self.Y          = Y
    self.cell_size  = size
    self.matrix     = [ [ [0, 0, 0, 0] for i in range(X / size) ] for j in range(Y / size)]

  def getCell(self, (x, y)):
    return self.matrix[int(x)][int(y)][0]

  def getCellColor(self, (x, y)):
    return self.matrix[int(x)][int(y)][1:]

  def setCell(self, (x, y), val):
    self.matrix[x][y][0] = val

  def setCellRaw(self, (x, y), val):
    x = (x + self.X / 2) / self.cell_size
    y = self.Y / self.cell_size - (y + self.cell_size + self.Y / 2) / self.cell_size
    self.setCell((int(x), int(y)), val)

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
          color = (0, 255 * self.getCell((i, j)), 255)

        screen.drawRectangleAbsolute(i * self.cell_size + 1,
                                     j * self.cell_size + 1,
                                     self.cell_size - 2,
                                     self.cell_size - 2,
                                     color)

  def draw(self, screen):
    self.drawScale(screen)
    self.drawMap(screen)
    screen.draw()
