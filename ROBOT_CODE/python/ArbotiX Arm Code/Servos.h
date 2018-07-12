// Pincher arm servo defs
#ifndef SERVOS_H
#define SERVOS_H

#include <avr/pgmspace.h>

#define SERVOCOUNT 5  //number of servos in this robot

// Servo ID's
#define BASE	1  // ID of base rotate servo
#define JOINT1	2  // ID of first joint servo
#define JOINT2	3  // ID of first joint servo
#define JOINT3	4  // ID of first joint servo
#define GRIPPER	5  // ID of gripper servo

// Servo min/max
static const PROGMEM uint16_t _Mins[] = {   0, 105,  30, 180,   0 };
static const PROGMEM uint16_t _Maxs[] = {1023, 925, 975, 870, 512 };

#define ServoMin(x)  pgm_read_word_near(_Mins+x-1)
#define ServoMax(x)  pgm_read_word_near(_Maxs+x-1)

// Servo punch
static const PROGMEM uint16_t _Punch[5] = { 50, 50, 50, 50, 32 };
#define ServoPunch(x)  pgm_read_word_near(_Punch+x-1)

// Compliance slope and margin
static const PROGMEM uint16_t _Slope[5] = { 32, 32, 32, 32, 128 };
static const PROGMEM uint16_t _Margin[5] = { 1, 1, 1, 1, 1 };
#define ServoSlope(x)  pgm_read_word_near(_Slope+x-1)
#define ServoMargin(x)  pgm_read_word_near(_Margin+x-1)

// Torques
static const PROGMEM uint16_t _Torque[5] = { 1023, 1023, 1023, 1023, 350 };
#define ServoTorque(x)  pgm_read_word_near(_Torque+x-1)

// Rotation defs
#define DEG_90 307	// Servo postion "ticks" for 90deg
// Arm dimension defs
// ***FIX***


#endif  // SERVOS_H

