import time

class Robot:
  def __init__(self, server, pos):
    self.sock   = server
    self.pos    = pos
    self.orient = (1, 0)

  def getPos(self):
    return self.pos

  def setPos(self, pos):
    self.pos = pos

  def setOrient(self, orient):
    self.orient = orient

  def rec(self, n):
    output = self.sock.recv(n)
    return output

  def send(self, string):
    self.sock.sendall(string)
    time.sleep(0.1)

  def recMeasurement(self):
    radius  = int(self.rec(8))
    angle   = float(self.rec(8))

    return (radius, angle)

  def sendTranslation(self, (x, y)):
    print "TRANSLATION : " + str(x) + " " + str(y)
    #self.send("T")
    #self.send(str(x))
    #self.send(str(y))

  def sendRotation(self, angle):
    print "ROTATION : " + str(angle)
    #self.send("R")
    #self.send(str(angle))
