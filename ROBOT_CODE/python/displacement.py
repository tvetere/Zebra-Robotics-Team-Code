#!/usr/bin/env python
import cv2
import numpy as np

fn = 'perfect'
img = cv2.imread(fn+'.jpg')
img = cv2.resize(img, (500, 500)) 
crop_img = img[250:500, 0:500] 
# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]

'''
for i in range(500):
    cv2.circle(crop_img, (i,250), 1, (255,255,0), 1)
'''

#for i in range(249):
    #cv2.circle(crop_img, (249,i), 1, (0,255,0), 1)

min = 1000
max = -1000
count = 0
for y in range(0, 249):
	col = crop_img[y,249]
	if (col[0]<50 and col[1]>90 and col[2]>90):
		count+=1

print(count)
print(count/249*100,"%")
#print(crop_img[150,0])   #y,x

cv2.imshow('crop', crop_img)
#cv2.imwrite(fn+'_new.jpg', edges)

cv2.waitKey(0)
cv2.destroyAllWindows()




