import create
import driver
import time
import math
import armcontrol
import cv2
import numpy as np
from picamera import PiCamera
from time import sleep
from camSet import clickImage
from camSet import processImage
from camSet import getDist1
from camSet import checkAlignment
from detectColor import findColor
from camSet import fillCol
camera = PiCamera()
camera.start_preview(fullscreen=False, window=(100,20,640,480))

driver = driver.Driver(3,1)
arm = armcontrol.ArmControl("/dev/ttyUSB1")
sleep(10)
arm.sendCmd("9")
sleep(2)
driver.driveTo(3,2,100)
clickImage()
crop_img = processImage()
color = findColor(crop_img)
print("color 1 : ",color)

driver.driveTo(3,4,100)
clickImage()
crop_img = processImage()
color = findColor(crop_img)
print("color 2 : ",color)

driver.driveTo(3,6,100)
clickImage()
crop_img = processImage()
color = findColor(crop_img)
print("color 3 : ",color)

driver.disable()

'''
def clickImage():	
	camera.start_preview(fullscreen=False, window=(100,20,640,480))
	i=1
	camera.capture('/home/pi/Robotics/Zebra-Robotics/python/test_pic.jpg')
	camera.stop_preview()
	
driver = driver.Driver(0,0)
arm = armcontrol.ArmControl("/dev/ttyUSB1")
sleep(10)
driver.driveTo(0,1,100)
arm.sendCmd("9")
sleep(2)
clickImage()

'''

#t0 = time.time()
#driver.turnSlightLeft(.2)
#driver.turnLeft()
#t1 = time.time()
#driver.turnLeft(100)

#print(t1-t0)



'''
driver functions:
driveForward: Only call for small movements. Does not update Roomba's internal position monitor
turnLeft:
turnRight:
turn180:
revcrawl: Go backwards very slowly
driveTo: Go to a specific point
driveScan: Starting procedure to scan buckets
disable: Stop the roomba and disable serial

#driver.driveForward(200,50)
#driver.driveTo(0,2, 100)
#driver.turnLeft()
#driver.driveTo(2,0,200)
'''