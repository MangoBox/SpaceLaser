#include<Arduino.h>
#include<stdio.h>
#include<string.h>
/*****************************************************************
GLOBAL VARIABLES:
*****************************************************************/
//Number of data point we are reciving
int NUM_DATAPT;
// Time interval between data points
int T_interval; 

//Main data type
struct horizon_co {
double az;
double alt;
// MAYBE TIME
};
