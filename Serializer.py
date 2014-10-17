import pickle

def save(filename, obj):
  """
  Serialize an object in a file. WARNING : if the file already exists, it will
  be erased.

  @type     filename  :   string
  @param    filename  :   name of the file to write
  @type     obj       :   Object
  @param    obj       :   object to be serialized
  """
  with open(filename, 'wb') as f:
    pickle.dump(obj, f)

def load(filename):
  """
  Deserialize an object serialized with the Serializer.save() method.
  If the file doesn't exist, an error will be raised.

  @type     filename  :   string
  @param    filename  :   file to read in
  """
  with open(filename, 'rb') as f:
    return pickle.load(f)
