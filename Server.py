import socket, sys, threading
import Trigo

class Server:
  def __init__(self, host, port):
    """
    Constructor for Server.

    @type     host  :   string
    @param    host  :   let it empty. Just pass '' as parameter
    @type     port  :   int
    @param    port  :   the port where socket has to listen
    """
    self.socket   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.threads  = []

    try:
      self.socket.bind((host, port))
    except socket.error:
      print 'Bind Failed.'
      sys.exit()
    print 'Bind OK.'

  def listen(self, n):
    """
    Start socket listening for n clients.

    @type     n   :   int
    @param    n   :   number of client the socket has to listen
    """
    self.socket.listen(n)

  def accept(self):
    """
    Wait for a client. This is a blocking call
    """
    conn, addr = self.socket.accept()
    return (conn, addr)

  def threadFunc(self, trgt, argv):
    """
    Start a method in a new thread.

    @type     trgt  :   method
    @param    trgt  :   the method to be run in a new thread
    @type     argv  :   (...,)
    @param    argv  :   arguments used to run the method
    """
    t = threading.Thread(target=trgt, args=argv)
    self.threads.append(t)
    t.start()

  def close(self):
    """
    Close the socket.
    """
    self.socket.close()
