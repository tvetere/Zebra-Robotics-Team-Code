// InterbotiX PhantomX Pincher Robotic Arm Demo

#include <ax12.h>               // Include base library for DYNAMIXELs
#include <BioloidController.h>  // Include bioloid libary for poses/movements
#include "poses.h"
#include "Servos.h"

BioloidController bioloid = BioloidController(1000000); //start the BIOLOID library at 1mbps. This will run the dxlInit() function internally, so we don't need to call it

int currentBasePos = BASE_POS;


void setup()
{
	pinMode(USER_LED,OUTPUT);  // Set LED pin as an output
	digitalWrite(USER_LED, HIGH); // Set LED high to show that the test has started

	Serial.begin(115200); // Open serial port to host
	Serial.setTimeout(31000); // Set serial timeout

	Serial.println("Starting PhantomX Pincher Robot Arm Test.");

	dxlServoReport(SERVOCOUNT);    // Scan Servos, return position and error (if there are any)

	digitalWrite(USER_LED, LOW); // Set LED low to show ready to go

	MoveTo(Center,1500);     // Move servos to home position
}

void loop()
{
 int Servo, Pos;
 int code = 0;
 int degree = 0;
 if (Serial.available() > 0) {
    // read the incoming byte:
    int incomingByte = Serial.read();
    code = incomingByte - '0';
    ShowPosistion();
    }
  // Send the code serially to :
  switch (code) {
    case 1:             
     MoveTo(Center,1500);                   // Move every motor to centre
    break;
    case 2:
      SetBase(BASE_POS);                    //Put the arm in pre-grab position                      
      MoveTo(Pick,1800);
     break;
    case 3:
      GrabBlock();                         //Grab the block
      dxlSetGoalPosition(GRIPPER,GRIPPER_GRAB);
      delay(1800);
      MoveTo(Take,500);
     break;
    case 4:                               //Put the odd block on the back
      MoveTo(Deliver,2000);
      DropBlock();
      delay(500);
     break;
    case 5:
      DropBlock();                       //Drop the block in a bin
      MoveTo(TakeUp,200);
    break;
    case 6:                              // Rotate base right to number of degrees specified on the serial port
      while (Serial.available() == 0){}
      degree = 0;
      if (Serial.available() > 0)
        {
          Serial.println("Coming Here");
          degree = Serial.read() - '0';
          Serial.println(degree);
        }
      MoveLeft(degree);
      delay(200);
     break;
     case 7:                          // Rotate base left to number of degrees specified on the serial port
      while (Serial.available() == 0){}
      degree = 0;
      if (Serial.available() > 0)
        {
          degree = Serial.read() - '0';
        }
      MoveRight(degree);
      delay(200);
     break;
      case 8:                         // Move the base motor to centre
      SetBase(BASE_POS);
      delay(200);
      break;
      case 9:                         // Scan the Color of the bins
      MoveTo(Identification,1800);
      break;
    default: 
      //MoveTo(Center,3000);
    break;
  }
}

void ShowPosistion(void)
{
	int cnt;

	Serial.println();
	for (cnt = 1; cnt <= 5; ++cnt)
	{
		Serial.print(cnt);
		Serial.print(": ");
		Serial.print(dxlGetPosition(cnt));
		Serial.print("   ");
	}
	Serial.println();
}

void GrabBlock(void)
{
  int j1 = 186;
  int j2 = 201;
  int j3 = 895;
  
  for(j3=895; j3<=921;j3++)
    SetPosition(JOINT3,j3++);
    
  while((j1 != 136 || j2 != 445) || (j3 != 627)){
    if(j1 != 136){
      SetPosition(JOINT1,j1--);
    }
    if(j2 != 445){
      SetPosition(JOINT2,j2++);
      j2++;
    }
    if(j3 != 627){
      SetPosition(JOINT3,j3--);
    }
    delay(5);
  }   
}

void DropBlock(void)
{
	dxlSetGoalPosition(GRIPPER,GRIPPER_OPEN);
	delay(800);
}

void MoveLeft(int degree)
{
  dxlSetGoalPosition(BASE,currentBasePos-degree);
  currentBasePos -= degree;
  delay(100);
}
void MoveRight(int degree)
{
  dxlSetGoalPosition(BASE,currentBasePos+degree);
  currentBasePos += degree;
  delay(100);
}

void SetBase(int Pos)
{
  dxlSetGoalPosition(BASE,Pos);
  currentBasePos = Pos;
  delay(200);
}

void MoveTo(const PROGMEM uint16_t *dest, uint16_t ms)
{
	bioloid.loadPose(dest);   // load the pose from FLASH, into the nextPose buffer
	bioloid.readPose();            // read in current servo positions to the curPose buffer
	bioloid.interpolateSetup(ms); // setup for interpolation from current->next over 1/2 a second
	while(bioloid.interpolating > 0)
	{  // do this while we have not reached our new pose
		bioloid.interpolateStep();     // move servos, if necessary.
		delay(33);
	}
}



void ConfigServos(int NumServos)
{
	int cnt;

	// Init servos
	for (cnt = 1; cnt <= NumServos; ++cnt)
	{
		dxlSetPunch(cnt,ServoPunch(cnt));
		axSetCCWComplainceSlope(cnt,ServoSlope(cnt));
		axSetCWComplainceSlope(cnt,ServoSlope(cnt));
		axSetCCWComplainceMargin(cnt,ServoMargin(cnt));
		axSetCWComplainceMargin(cnt,ServoMargin(cnt));
		dxlSetRunningTorqueLimit(cnt,ServoTorque(cnt));
	}
}
