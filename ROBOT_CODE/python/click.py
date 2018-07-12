import create
import driver
from time import sleep
import math
import armcontrol
import cv2
from picamera import PiCamera
camera = PiCamera()

driver = driver.Driver(0,0)
arm = armcontrol.ArmControl("/dev/ttyUSB1")
def clickImage():	
	camera.start_preview()
	#sleep(2)
	#for i in range(5):
	i=1
	camera.capture('/home/pi/Robotics/Zebra-Robotics/python/pic%s.jpg' % i)
	camera.stop_preview()
	#sleep(2)
sleep(10)
arm.sendCmd("2")

sleep(7)

clickImage()

driver.disable()
