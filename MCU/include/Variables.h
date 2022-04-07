#include<Arduino.h>
#include<stdio.h>
/*****************************************************************
GLOBAL VARIABLES:
*****************************************************************/
//Number of data point we are reciving
const int NUM_DATAPT = 50;

//Main data type
struct horizon_co {
double az;
double alt;
};
