import serial

class ArmControl:
    def __init__(self, PORT="/dev/ttyUSB0"):
        self.ser = serial.Serial(PORT, 115200, timeout=0.5)
        if  self.ser.isOpen():
            print 'Serial port did open, presumably to an arm...'

    def sendCmd(self, sig):
      print "sent cmd " , sig
      self.ser.write(sig)
