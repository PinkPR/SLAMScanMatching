import math
import Serializer
import ScanMatching
import OdoCorrection

pointset1 = Serializer.load("pointset1")
pointset2 = Serializer.load("pointset2")
q = (0, 0, math.pi / 2)
ScanMatching.applyQList(pointset2, (0, 0, -math.pi / 2))

qmin = OdoCorrection.getMin(pointset2, pointset1, q)
