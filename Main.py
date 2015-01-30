from threading import *
import Server
import Screen
import Map

screen  = Screen.Screen(800, 800, 300, 300)
mmap    = Map.Map(300, 300, 5)
pos     = [0, 0, 0]

measurements = []

server = Server.Server('', 8888)
server.listen(1)
connaddr = server.accept()

def thrd(conn):
  ret = server.handleCommand(conn)

  while ret:
    if ret[0] == 'T':
      pos[0] = pos[0] + ret[1][0]
      pos[1] = pos[1] + ret[1][1]
    elif ret[0] == 'R':
      pos[2] = pos[2] + ret[1][0]
    elif ret[0] == 'M':
      measurements.append(ret[1])

server.threadFunc(thrd, (connaddr[0],))

while True:
  mmap.draw(screen)
