import math
import Serializer
import ScanMatching

pointset1 = Serializer.load("pointset1")
pointset2 = Serializer.load("pointset2")
q = (0, 0, 0)
ScanMatching.applyQList(pointset2, (0, 0, math.pi / 2))

qmin = ScanMatching.runScanMatching(pointset1, pointset2, q)
