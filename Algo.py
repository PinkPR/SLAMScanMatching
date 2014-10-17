def mapList(func, lst):
  for i in range(len(lst)):
    lst[i] = func(lst[i])
