# Zebra-Robotics   
  
All code is in the Python folder.   
The other folders are example code in other languages.



Main.py is the main entry point to the program   
Armcontrol.py is the serial connection to the arm. Here, commands should be sent to the arm   
create.py is the API for the roomba   
driver.py is the driving program for the roomba   
binmanager.py is for keeping track of the bins as we scan them when we start   
reset.py disables the roomba if it misbehaves. Always call this when done with the roomba for the day, otherwise battery will die   


To run from python shell, do   
import create    
driver = driver.Driver(0,0)   
Then enter function to call in driver.py   


driver functions:   
driveForward: Only call for small movements. Does not update Roomba's internal position monitor   
turnLeft:   
turnRight:    
turn180:   
revcrawl:  Go backwards very slowly   
driveTo: Go to a specific point   
driveScan: Starting procedure to scan buckets   
disable:   Stop the roomba and disable serial   

driver.py is only for driving functions. Any arm control should be done in main.py   
in main.py should be lines telling it to driveTo(x,y), inch forward, grab, move, drop, etc   
