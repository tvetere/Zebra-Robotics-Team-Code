import create
import driver
from sense_hat import SenseHat
import bucket
from color import Color
import binmanager
from time import sleep
import time
import math
from detectColor import findColor
from camSet import clickImage
from camSet import processImage1
from camSet import processImage

class Direction:
    NORTH = 0
    WEST = 1
    SOUTH =2
    EAST = 3

wheelError = .15

class Driver:
    def __init__(self, x, y, binman,  port="/dev/ttyUSB1"):
        self.xpos = x;
        self.ypos=y;
        self.orientation = Direction.NORTH
        self.robot = create.Create(port, 115200,create.FULL_MODE)
        self.bm = binman

    #type = 0: use distance only for stopping
    #type = 1: use sensors for stopping, plus dist thresh
    #type = 2: use sensors for stopping only, no dist thresh
    def driveForward(self, speed, distance, type = 1):
        currDist=0
        startDist=abs(self.robot.sensors([create.DISTANCE])[19])
        startDist=abs(self.robot.sensors([create.DISTANCE])[19])
        startDist=abs(self.robot.sensors([create.DISTANCE])[19])
        print "start dist " , startDist
        distance+=startDist
        lastLeft = self.robot.sensors([create.ENCODER_LEFT])[43]
        lastRight = self.robot.sensors([create.ENCODER_RIGHT])[44]
        #Drive until we either see a line, or reach a max distance
        while 1:
            speedL = speed
            speedR = speed
            currDist+=abs(self.robot.sensors([create.DISTANCE])[19])
            #print ("curr dist = ", currDist, ", desired: ", distance)
            if (type == 0 or type == 1 )and currDist >= distance :
                print "----------------------Distance-Based Stop!----------------------"
                self.robot.stop()
                return
            #grab encoder values and find encoder delta
            left = self.robot.sensors([create.ENCODER_LEFT])[43]
            right = self.robot.sensors([create.ENCODER_RIGHT])[44]
            dleft = left-lastLeft
            dright=right-lastRight
            #print ( "Encoder deltas: Left, Right: " , dleft ,dright)

            if dleft > -10000 and dleft  <10000 and dright > -10000 and dright < 10000:   
                if dright > dleft :
                    #right wheel moved to much, speed up left side
                    adjust =(dright -dleft)/2
                    if adjust < -20:
                        adjust = -20
                    speedL = speedL + adjust*1.1
                    speedR = speedR - adjust
                    
                else:
                    #left wheel moved too much, speed up right side
                    adjust =(dleft -dright)/2
                    if adjust > 20:
                        adjust = 20
                    speedL = speedL -adjust
                    speedR = speedR + adjust*1.1
               
            
            
            #print("Left WV = ", float(speedL/10), ", Right WV = " , float(speedR)/10)
            self.robot.setWheelVelocities(  speedL/float(10), speedR/float(10)+wheelError)
            
            

            #grab info about the lines
            info = self.robot.sensors([create.CLIFF_LEFT_SIGNAL,
                                     create.CLIFF_FRONT_LEFT_SIGNAL,
                                     create.CLIFF_FRONT_RIGHT_SIGNAL,
                                     create.CLIFF_RIGHT_SIGNAL])
            #print "BL IR Sensor - " , info[28] , "BR IR Sensor - " , info[31]
            if distance-currDist > 6 : #and currDist-startDist > 10:
                #only inspect when in middle of square, otherwise cross lines mess this up
                if info[29] < 2400 and info[30] > 2400:
                     #turned too much right, so turn right wheel hard
                     self.robot.setWheelVelocities(  speed/float(10), speed/float(10)+5)
                     print ("******************see left line****************")
                     sleep(.1)
                     lastLeft = self.robot.sensors([create.ENCODER_LEFT])[43]
                     lastRight = self.robot.sensors([create.ENCODER_RIGHT])[44]
                if info[30] < 2400 and info[29] > 2400:
                    #turned too much left, so turn left wheel hard
                    self.robot.setWheelVelocities(  speed/float(10)+5, speed/float(10))
                    print ("*********************see rightline************************")
                    sleep(.1)
                    lastLeft = self.robot.sensors([create.ENCODER_LEFT])[43]
                    lastRight = self.robot.sensors([create.ENCODER_RIGHT])[44]
            info = self.robot.sensors([create.CLIFF_LEFT_SIGNAL,
                         create.CLIFF_FRONT_LEFT_SIGNAL,
                         create.CLIFF_FRONT_RIGHT_SIGNAL,
                         create.CLIFF_RIGHT_SIGNAL])
            if info[28] <2400 or info[31] <2400 :
                print "BL IR Sensor - " , info[28] , "BR IR Sensor - " , info[31]
                #if either the back left or back right sensor see a line, stop

                #if we traveled at least 10cm, then stop.
                #this check needed b/c if left sensor caused previous stop,
                # right sensor could immediately stop this iteration
                if info[28] < 2400 and info[31] < 2400:
                      s=0
                elif info[28] < 2400:
                      s = 1
                else:
                      s=2
                      
                #if doing line-based stopping
                if (type == 2 or type == 1)and currDist > 12:
                    #see a line
                    #self.robot.stop()
                    print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!hit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    t1 = time.time()
                    while s!=0:
                         info = self.robot.sensors([create.CLIFF_LEFT_SIGNAL,
                                     create.CLIFF_FRONT_LEFT_SIGNAL,
                                     create.CLIFF_FRONT_RIGHT_SIGNAL,
                                     create.CLIFF_RIGHT_SIGNAL])
                         if s == 1 and info[31] < 2400 :
                             print "turing slight left with time: " , time.time() - t1
                             self.turnSlightLeft((time.time()-t1), 50)
                             break
                         elif s == 2 and info[28] < 2400 :
                             print "turing slight right with time: " , time.time() - t1
                             self.turnSlightRight((time.time()-t1), 50)
                             break
                             
                         t2 = time.time()
                         
                         if (t2 - t1) > .5 :
                             print "timed out!!!!!!!!"
                             break
                    '''
                    if info[31] <2400:
                        print ("left too far back")
                        self.robot.setWheelVelocities(  speed/float(10)+5, 0)
                        sleep(.15)
                    else:
                        print ("right too far back")
                        self.robot.setWheelVelocities(  0, speed/float(10)+5)
                        sleep(.15)
                    '''
                    
                    return
                else :
                    #if we got a hit too soon, then we are not straight, so adjust
                    if info[31] <2400:
                        print ("left too far back")
                        self.robot.setWheelVelocities(  speed/float(10)+2, speed/float(10))
                        sleep(.1)
                        lastLeft = self.robot.sensors([create.ENCODER_LEFT])[43]
                        lastRight = self.robot.sensors([create.ENCODER_RIGHT])[44]
                    else:
                        print ("right too far back")
                        self.robot.setWheelVelocities(  speed/float(10), speed/float(10)+2)
                        sleep(.1)
                        lastLeft = self.robot.sensors([create.ENCODER_LEFT])[43]
                        lastRight = self.robot.sensors([create.ENCODER_RIGHT])[44]
            #if distance based stopping, then we need to sleep longer else distance value stays 0
            if type != 0:
                sleep(.04)
            else :
                sleep(.1)
            #28-31

    def turnSlightLeft(self,slp, speed = 100):
       
        self.robot.setWheelVelocities(-speed/float(10), speed/float(10))
        sleep(slp)
        self.robot.stop()

    def turnSlightRight(self,slp, speed = 100):
      
        self.robot.setWheelVelocities(speed/float(10), -speed/float(10))
        sleep(slp)
        self.robot.stop()

    def turnLeft(self, speed=100):
        hit = 0
        counter = 0
        print "turning"
        while 1:

            self.robot.setWheelVelocities(  -speed/float(10), speed/float(10))
             #28-31
            info = self.robot.sensors([create.CLIFF_LEFT_SIGNAL,
                                     create.CLIFF_FRONT_LEFT_SIGNAL,
                                     create.CLIFF_FRONT_RIGHT_SIGNAL,
                                     create.CLIFF_RIGHT_SIGNAL])
            if hit==0 and info[30] <2400:
                hit = 1
                sleep(.1)
                print("hit")
            elif (hit == 1 and counter > 25) and info[29] < 2400:
                sleep(.1)
                self.updateRotCCW()
                self.robot.stop()
                return
            elif (hit == 1 and counter > 25) and info[30] < 2400:
                self.robot.setWheelVelocities(  speed/float(10), -speed/float(10))
                sleep(.1)
                self.updateRotCCW()
                self.robot.stop()
                return
            sleep(.02)
            counter += 1

    def turnRight(self, speed=100):

        hit = 0
        counter = 0
        while 1:
            print counter
            self.robot.setWheelVelocities(  speed/float(10),-speed/float(10))
             #28-31
            info = self.robot.sensors([create.CLIFF_LEFT_SIGNAL,
                                     create.CLIFF_FRONT_LEFT_SIGNAL,
                                     create.CLIFF_FRONT_RIGHT_SIGNAL,
                                     create.CLIFF_RIGHT_SIGNAL])
            if hit==0 and info[29] <2400:
                hit = 1
                sleep(.1)
                print("hit")
            elif (hit == 1 and counter > 25) and info[30] < 2400 :
                sleep(.1) #empirically adjusted to center on line
                self.updateRotCW()
                self.robot.stop()
                return
            elif (hit == 1 and counter > 25) == 1 and info[29] < 2400 :
                self.robot.setWheelVelocities(-speed/float(10),speed/float(10))
                sleep(.1)
                self.updateRotCW()
                self.robot.stop()
                return

            sleep(.02)
            counter += 1

    def turn180(self, speed = 100):
        hit = 0
        while 1:
            self.robot.setWheelVelocities(  -speed/float(10), speed/float(10))
             #28-31
            info = self.robot.sensors([create.CLIFF_LEFT_SIGNAL,
                                     create.CLIFF_FRONT_LEFT_SIGNAL,
                                     create.CLIFF_FRONT_RIGHT_SIGNAL,
                                     create.CLIFF_RIGHT_SIGNAL])
            if hit==0 and info[30] <2400:
                hit = 1
                sleep(.1)
                print("hit")
            elif hit ==1 and info[30] < 2400:
                hit = 2
                sleep(.1)
                print("hit")
            elif hit == 2 and info[29] < 2400:
                sleep(.1)
                self.updateRotCCW()
                self.robot.stop()
                return
            elif hit == 2 and info[30] < 2400:
                self.robot.setWheelVelocities(  speed/float(10), -speed/float(10))
                sleep(.1)
                self.updateRotCCW()
                self.robot.stop()
                return
            sleep(.02)

    def revcrawl(self,dist,speed):
        currDist=0
        startDist=abs(self.robot.sensors([create.DISTANCE])[19])
        while 1:
            currDist+=abs(self.robot.sensors([create.DISTANCE])[19])
            self.robot.setWheelVelocities(  -speed/float(10),-speed/float(10))
            info = self.robot.sensors([create.CLIFF_LEFT_SIGNAL,
                                     create.CLIFF_FRONT_LEFT_SIGNAL,
                                     create.CLIFF_FRONT_RIGHT_SIGNAL,
                                     create.CLIFF_RIGHT_SIGNAL])
            if info[28] <2400 or info[31] <2400 or currDist >=dist-startDist:
                self.robot.stop()
                return
        


        
        
    #drive to an x and y position on the game board
    def driveTo(self, x, y, speed=100):
        print "x:", self.xpos , ", y:", self.ypos, ", rot:" , self.orientation

        if y > self.ypos:
            #head north
            if self.orientation == 3 :
                #if facing east, turn left
                #move forward a little, so we end up on line after turn 
                self.robot.setWheelVelocities(  speed/float(10), speed/float(10))
                sleep(.5) #empirically adjusted
                self.turnLeft()         
            elif self.orientation == 1 :
                #if facing west, turn right
                #move forward a little, so we end up on line after turn 
                self.robot.setWheelVelocities(  speed/float(10), speed/float(10))
                sleep(.5) #empirically adjusted
                self.turnRight()
            elif self.orientation == 2:
                #if facing south, turn around
                #move forward a little, so we end up on line after turn 
                self.robot.setWheelVelocities(  speed/float(10), speed/float(10))
                sleep(.5) #empirically adjusted
                self.turnRight()
                self.turnRight()
            diff = y - self.ypos
            for z in range(0,diff):
                self.driveForward(speed, 41)
                self.updateXY()
                print "z:", z, ", x:", self.xpos , ", y:", self.ypos, ", rot:" , self.orientation

            self.robot.stop()
        elif y < self.ypos:
            #head south
            if self.orientation == 1 :
                #if facing west, turn left
                #move forward a little, so we end up on line after turn 
                self.robot.setWheelVelocities(  speed/float(10), speed/float(10))
                sleep(.5) #empirically adjusted
                self.turnLeft()

            elif self.orientation == 3 :
                 #if facing east, turn right
                #move forward a little, so we end up on line after turn 
                self.robot.setWheelVelocities(  speed/float(10), speed/float(10))
                sleep(.5) #empirically adjusted
                self.turnRight()

            elif self.orientation == 0:
                #if facing north, turn around
                #move forward a little, so we end up on line after turn 
                self.robot.setWheelVelocities(  speed/float(10), speed/float(10))
                sleep(.5) #empirically adjusted
                self.turnRight()
                self.turnRight()
           
            diff = self.ypos - y
            for z in range(0, diff):
                self.driveForward(speed,41)
                self.updateXY()
                print "z:", z, ", x:", self.xpos , ", y:", self.ypos, ", rot:" , self.orientation

            self.robot.stop()
    
        #fix x direction now
        
        
        if x < self.xpos:
            #turn to proper direction
            #need to head to head west
            if self.orientation == 0 :
                #move forward a little, so we end up on line after turn 
                self.robot.setWheelVelocities(  speed/float(10), speed/float(10))
                sleep(.5) #empirically adjusted
                self.turnLeft()
            elif self.orientation == 2 :
                #move forward a little, so we end up on line after turn 
                self.robot.setWheelVelocities(  speed/float(10), speed/float(10))
                sleep(.5) #empirically adjusted
                self.turnRight()
            elif self.orientation == 3:
                 #move forward a little, so we end up on line after turn 
                self.robot.setWheelVelocities(  speed/float(10), speed/float(10))
                sleep(.5) #empirically adjusted
                self.turnRight()
                self.turnRight()

            diff = self.xpos - x
            for z in range(0, diff):
                self.driveForward(speed, 41)
                self.updateXY()
                print " --------------------------------------------"
                print "z:", z, ", x:", self.xpos , ", y:", self.ypos, ", rot:" , self.orientation
            self.robot.stop()
        elif x > self.xpos:
           
            #turn to proper direction
            #need to head to head east
            if self.orientation == 2 :
                 #move forward a little, so we end up on line after turn 
                self.robot.setWheelVelocities(  speed/float(10), speed/float(10))
                sleep(.5) #empirically adjusted
                self.turnLeft()
            elif self.orientation == 0 :
                 #move forward a little, so we end up on line after turn 
                self.robot.setWheelVelocities(  speed/float(10), speed/float(10))
                sleep(.5) #empirically adjusted
                self.turnRight()
            elif self.orientation == 1:
                 #move forward a little, so we end up on line after turn 
                self.robot.setWheelVelocities(  speed/float(10), speed/float(10))
                sleep(.5) #empirically adjusted
                self.turnRight()
                self.turnRight()
            diff = x -self.xpos
            for z in range(0, diff):
                self.driveForward(speed, 41)
                self.updateXY()
                print " --------------------------------------------"
                print "z:", z, ", x:", self.xpos , ", y:", self.ypos, ", rot:" , self.orientation

            self.robot.stop()
            
                          
    def updateRotCCW(self):
        if self.orientation >= 3:
            self.orientation = -1
        self.orientation = self.orientation +1

    def updateRotCW(self):
        if self.orientation <= 0:
            self.orientation = 4
        self.orientation = self.orientation -1
        
    def updateXY(self):
        if self.orientation ==0 :
            #heading north, so increment y
            self.ypos = self.ypos+1
        elif self.orientation == 1 :
            #heading west, decrement x
            self.xpos = self.xpos-1
        elif self.orientation ==2 :
            self.ypos = self.ypos-1
        else :
            #heading east, increment x
            self.xpos = self.xpos +1

    #drive forward, scanning bins
    def driveScan(self, speed = 100):
        
            self.driveForward(speed, 41)
            self.updateXY()
           
            #grab frame and process
            self.robot.stop()
            clickImage()
            crop_img= processImage1()
            color = findColor(crop_img)
            #sleep(2)
            print ( "color = " , color)         
            self.bm.addBin(self.xpos, self.ypos, color)

            self.driveForward(speed, 41)
            self.updateXY()
            self.driveForward(speed, 41)
            self.updateXY()
            self.robot.stop()
            #grab frame and process
            clickImage()
            crop_img= processImage1()
            color = findColor(crop_img)
            #sleep(2)
            print ( "color = " ,color)
            self.bm.addBin(self.xpos, self.ypos, color)

            self.driveForward(speed, 41)
            self.updateXY()
            self.driveForward(speed, 41)
            self.updateXY()
            self.robot.stop()
            print "x:", self.xpos , ", y:", self.ypos
            #grab frame and process
            clickImage()
            crop_img= processImage1()
            color = findColor(crop_img)
            print ( "color = " ,color)
            self.bm.addBin(self.xpos, self.ypos, color)

    def disable(self):
        print ("disable")
        self.robot.toSafeMode()
        self.robot.close()

    def getPos(self):
        return [self.xpos, self.ypos]