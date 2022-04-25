#include<Arduino.h>
#include<stdio.h>
#include<string.h>
//Our head files
#include <Variables.h>
#include <Functions.h>


/*****************************************************************
MAIN
*****************************************************************/
void setup(){
    // Time to wait for serial data
    int wait_period = 306000;

    Serial.begin(9600);
    Serial.setTimeout (wait_period);
}

void loop(){
    /*Local variables*/
    struct horizon_co recieved_co [NUM_DATAPT];
    struct horizon_co current_co, delta_co ;
    
    delta_co = calulate_delta (current_co, recieved_co[0]);
}