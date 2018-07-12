#ifndef POSES_H
#define POSES_H

#include <avr/pgmspace.h>
#define BASE_POS 512
   
static const PROGMEM uint16_t Center[] = {5,  512,  512,  512,  640,  8};
static const PROGMEM uint16_t Identification[] = {5,  824,  105,  545,  663,  8};
static const PROGMEM uint16_t Pick[] =   {5,  512,  187,  201,  894,  512};
static const PROGMEM uint16_t Home[] =   {5,  512,  376, 1000,  430,  512};
static const PROGMEM uint16_t Take[] =   {5,  512,  382, 380,  480,  8};
static const PROGMEM uint16_t TakeUp[] = {5,  512,  382, 380,  480,  512};
static const PROGMEM uint16_t Drop[] =   {5,  512,  330, 380,  480,  100};
static const PROGMEM uint16_t Grab[] =   {5,  512,  136, 465,  577,  512};
static const PROGMEM uint16_t Deliver[] = {5, 578, 459, 793, 975, 8};


/////////////////////////////////////
static const PROGMEM uint16_t Demo1[] =  {4,  700,  600,  712,  712};
static const PROGMEM uint16_t Demo2[] =  {4,  400,  330,  312,  312};
static const PROGMEM uint16_t Demo3[] =  {4,  512,  800,  512,  512};
static const PROGMEM uint16_t Demo4[] =  {4,  512,  800,  512,  819};
static const PROGMEM uint16_t Demo5[] =  {4,    0,  376, 1000,  430};
static const PROGMEM uint16_t Demo6[] =  {4, 1023,  376, 1000,  430};

static const PROGMEM uint16_t OverLeft[] =  {4, 327,  555,  910,  655};
static const PROGMEM uint16_t DownLeft[] =  {4, 327,  610,  905,  615};

static const PROGMEM uint16_t OverCenter[] =  {4, 512,  710,  630,  758};
static const PROGMEM uint16_t DownCenter[] =  {4, 512,  753,  650,  716};

static const PROGMEM uint16_t OverRight[] =  {4, 681,  555,  910,  655};
static const PROGMEM uint16_t DownRight[] =  {4, 681,  610,  905,  615};

#define GRIPPER_GRAB 8 // Grab a block level
#define GRIPPER_OPEN 512 // Open gribber

#endif  // POSES_H
