#!/usr/bin/env python
import cv2
import numpy as np
from picamera import PiCamera
from time import sleep
from detectColor import findColor
camera = PiCamera()

def clickImage():	
	camera.start_preview(fullscreen=False, window=(100,20,640,480))
	i=1
	camera.capture('/home/pi/Robotics/Zebra-Robotics/python/pic%s.jpg' % i)
	camera.stop_preview()
	#sleep(2)

def processImage():
	fn = 'pic1'
	img = cv2.imread(fn+'.jpg')
	img = cv2.resize(img, (500, 500)) 

	#check crop and rotation
	M = cv2.getRotationMatrix2D((500/2,500/2),180,1)
	img = cv2.warpAffine(img,M,(500,500))
	crop_img = img[250:500, 0:500] 

	#cv2.imwrite(fn+'.jpg', crop_img)

	# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]

        #vertical mid line of image
        '''
	for i in range(250):
 	   cv2.circle(crop_img, (249,i), 1, (255, 255,255), 1)
        '''
	return crop_img

def processImage1():
	fn = 'pic1'
	img = cv2.imread(fn+'.jpg')
	img = cv2.resize(img, (500, 500)) 

	#cv2.imwrite(fn+'.jpg', img)
        return img


def fillCol(crop_img):
    for y in range(0,249):  #240,241
        for x in range(0, 499):
            col = crop_img[y,x]            
            if (col[0]<50 and col[1]<50 and col[2]>70):  #B, G, R
                #print(x,y,"RED")
                cv2.circle(crop_img, (x,y), 1, (255,255,255), 5)
    cv2.imwrite('new.jpg', crop_img)

def getDist1(crop_img, color):
    min = 1000
    max = -1000
    #print("inside getDist1, color : ",color)
    a = 230
    b = 250
    if color==3:
        a = 130
        b = 170
    for y in range(a,b):  #230, 250
        for x in range(0, 499):
            col = crop_img[y,x]
            if color==1:    #RED
                if (col[0]>0 and col[0]<20 and col[1]>0 and col[1]<50 and col[2]>60 and col[2]<255):
                    if(x<min):
                        min=x
                    if(x>max):
                        max=x
                    #cv2.circle(crop_img, (x,y), 1, (255,0,0), 2)
            elif color==3:    #BLUE
                if (col[0]>50 and col[0]<255 and col[1]>0 and col[1]<50 and col[2]>0 and col[2]<50):
                    if(x<min):
                        min=x
                    if(x>max):
                        max=x
            elif color==2:    #GREEN
                if (col[0]>0 and col[0]<50 and col[1]>50 and col[1]<255 and col[2]>0 and col[2]<50):
                    if(x<min):
                        min=x
                    if(x>max):
                        max=x
            elif color==0:    #YELLOW
                if (col[0]>0 and col[0]<46 and col[1]>41 and col[1]<242 and col[2]>100 and col[2]<255):
                    if(x<min):
                        min=x
                    if(x>max):
                        max=x
    
    #highlight min and max points   
    #cv2.circle(crop_img, (min,y), 1, (255,255,255), 2)
    #cv2.circle(crop_img, (max,y), 1, (255,255,255), 2)
    #print(min,max)
    temp = (int)((min+max)/2)
    #draw line at mid of min and max
    '''
    for i in range(250):
        cv2.circle(crop_img, (temp,i), 1, (255,255,255), 1)
    '''
    #print("temp=",temp)
    dist = temp - 249
    #print("dist=",dist)
    #cv2.imwrite('new.jpg', crop_img)       
    return dist

def checkAlignment(dist, color):
    
    if color==3:
        if dist>40 and dist <= 55 and dist != -249:  #right arm
            return 1
        elif dist<-20 and dist >= -35 and dist != -249: #left arm
            return 2
        elif dist < -35 and dist != -249: #left bot
            return 3
        elif dist > 55 and dist != -249: #right bot
            return 4
        elif dist>=-20 and dist<=40:
            return 0
        elif dist == -249:
            return -1
    else:
        if dist>40 and dist <= 55 and dist != -249:  #right arm
            return 1
        elif dist<-25 and dist >= -40 and dist != -249: #left arm
            return 2
        elif dist < -40 and dist != -249: #left bot
            return 3
        elif dist > 55 and dist != -249: #right bot
            return 4
        elif dist>=-25 and dist<=40:
            return 0
        elif dist == -249:
            return -1

'''
#crop_img = processImage()
file = 'grab_19.jpg'
crop_img = cv2.imread(file)
color = findColor(file)  # 0-red, 1-green, 2-blue, 3-yellow
#fillCol(crop_img)
dist = getDist1(crop_img, color)
'''



