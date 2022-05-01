#include<Arduino.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include <iostream>
#include <cstdlib>
//Our header files
#include <Variables.h>
#include <Functions.h>

void setup(){
    // Local variables
    int wait_period = 306000;
    int baud_rate = 9600;

    //Starting serial
    Serial.begin(baud_rate);
    Serial.setTimeout (wait_period);
}

void loop(){
    /*Local variables*/
    char Raw_Data[80] = "133.193231,-27.095697,2022-04-29,22:07:06";
    struct horizon_co recieved_co [NUM_DATAPT];
    //struct horizon_co current_co, delta_co ;
    
    //Recieving data from cpu
    /*
    while(Serial.available() == 0);
    Raw_Data = Serial.readStringUntil('\r');
    Serial.setTimeout(0.01);
    */

    //Extracting Data from raw data
    Serial.println (Raw_Data);
    String_strtok (Raw_Data, recieved_co[1], Strtok_outputs);
    delay (5000);

}