import color
import bucket

class BinManager:
    def __init__(self):
        self.binlist= []
    def addBin(self,x, y, color):
        self.binlist.append(bucket.Bucket(x, y, color))

    def getPosByColor(self,color):
        for e in self.binlist:
            if e.getColor() == color:
                return [e.getX(), e.getY()]
        return [-1,-1]
    
                         
    
