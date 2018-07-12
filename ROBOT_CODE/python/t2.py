from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(2)
for i in range(5):    
    camera.capture('/home/pi/Robotics/Zebra-Robotics/python/test_image%s.jpg' % i)
camera.stop_preview()
