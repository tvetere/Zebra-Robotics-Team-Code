import numpy as np
import cv2
from color import Color
    
lower_blue = np.array([50, 0, 0])   #50,0,0                                  
upper_blue = np.array([255, 50, 50])

lower_yellow = np.array([0,41,100]) #100,41,0
upper_yellow = np.array([46,242,255])#255,242,46

lower_red = np.array([0,0,60])#100,100,0
upper_red = np.array([20,50,255])#255,255,20

lower_green = np.array([0,50,0])
upper_green = np.array([50,255,50])

def findRed(img):
    mask = cv2.inRange(img, lower_red, upper_red)
    count = cv2.countNonZero(mask)
    print("No of red pixels---->",count)
    return count

def findYellow(img):
    mask = cv2.inRange(img, lower_yellow, upper_yellow)
    count = cv2.countNonZero(mask)
    print("No of yellow pixels---->",count)
    return count

def findBlue(img):
    mask = cv2.inRange(img, lower_blue, upper_blue)
    count = cv2.countNonZero(mask)
    print("No of blue pixels---->",count)
    return count
    
def findGreen(img):
    mask = cv2.inRange(img, lower_green, upper_green)
    count = cv2.countNonZero(mask)
    print("No of green pixels---->",count)
    return count


def findColor(img):
    #img = cv2.imread(file)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    r = findRed(img)
    g = findGreen(img)
    b = findBlue(img)
    y = findYellow(img)
    arr = [r,g,b,y]
    '''
    max = arr[0]
    pos = 0
    for i in range(1,4):
        if arr[i] > max:
            max = arr[i]
            pos = i
    '''
    maxi = max(arr)
    pos = arr.index(maxi)
    colors = [Color.RED,Color.GREEN, Color.BLUE, Color.YELLOW]
    print("COLOR DETECTED - ", pos, colors[pos])
    return colors[pos]
    #return pos

#findColor("blue.jpg")