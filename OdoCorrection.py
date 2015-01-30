import ScanMatching
import copy
import math

def getErrorSum(cp_list):
  error_sum = 0

  for i in range(len(cp_list)):
    x = cp_list[i][0][0] - cp_list[i][1][0]
    y = cp_list[i][0][1] - cp_list[i][1][1]
    error_sum = error_sum + (math.hypot(x, y))

  return error_sum

def getValuesAround(val, percent, nb):
  result  = []
  step    = (val * (1.0 + percent / 100.0) - val) / nb

  for i in range(nb):
    result.append(val * (1.0 - percent / 100.0) + i * step)

  return result

def getMin(new, ref, q):
  qmin  = (0, 0, 0)
  match = []
  tmp   = []
  error = float("+inf")

  for i in getValuesAround(q[0], 10, 10):
    for j in getValuesAround(q[1], 10, 10):
      for k in getValuesAround(q[2], 10, 10):
        tmp = copy.deepcopy(new)
        ScanMatching.applyQList(tmp, (i, j, k))
        match = ScanMatching.matchPoints(ref, tmp, tmp)
        tmp_error = getErrorSum(match)

        if (tmp_error < error):
          print "QMIN FOUND !"
          error = tmp_error
          qmin = (i, j, k)
          print qmin

  return qmin
