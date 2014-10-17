import sys
import socket
import subprocess

from naoqi import *

s = socket.socket(soket.AF_INET, socket.SOCK_STREAM)
s.connect((argv[1], int(argv[2]))

output = subprocess.Popen(["/home/nao/picocom", "-b", "9600", "/dev/ttyUSB0"],
                          stdout=subprocess.PIPE).communicate()[0]

s.sendall(output)
s.sendall("0")

s.close()
