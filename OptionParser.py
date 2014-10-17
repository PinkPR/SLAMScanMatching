import time

class OptionParser:
  def __init__(self, argv):
    """
    Constructor for OptionParser. Detects if the -load or -save options are
    present. If yes, the constructor sets the fields appropriately. Options
    -load and -save can't be used simultaneously or -load will be supplanted
    by -save.

    @type     argv  :   [string]
    @param    argv  :   sys.argv
    """
    self.argv     = argv
    self.load     = False
    self.save     = False
    self.filename = ''

    if ('-load' in argv):
      self.load = True
      self.filename = argv[argv.index('-load') + 1]

    if ('-save' in argv):
      self.save = True
      self.filename = argv[argv.index('-save') + 1] + time.strftime("%Y%m%d.%H.%M.%S") + ".pck"
