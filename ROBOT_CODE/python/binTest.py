import bucket
from color import Color
import binmanager

bm = binmanager.BinManager()
bm.addBin(0,0,Color.GREEN)
bm.addBin(1,0,Color.RED)
bm.addBin(0,3,Color.YELLOW)

print bm.getPosByColor(Color.GREEN)
print bm.getPosByColor(Color.RED)
print bm.getPosByColor(Color.BLUE)
