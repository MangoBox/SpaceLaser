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
    char Raw_Data_1[55] = "133.193231,-27.095697,2022-04-29,22:07:06";
    char Raw_Data_2[55] = "180.123433,-95.900123,2022-04-29,22:07:11";
    
    struct horizon_co recieved_co [NUM_DATAPT];
    struct horizon_co current_co, delta_co ;
    
    //Recieving data from computer program
    /*
    while(Serial.available() == 0);
    Raw_Data = Serial.readStringUntil('\r');
    Serial.setTimeout(0.01);
    */

    //Extracting Data Strings from raw data
    Serial.print ("Raw data string 1 = ");
    Serial.println (Raw_Data_1);
    
    recieved_co[1] = String_strtok (Raw_Data_1, Strtok_outputs);
    Serial.println (recieved_co[1].alt);
    Serial.println (recieved_co[1].az);
    delay (5000);

    Serial.print ("Raw data string 2 = ");
    Serial.println (Raw_Data_2);
    
    recieved_co[2] = String_strtok (Raw_Data_2, Strtok_outputs);;
    Serial.println (recieved_co[2].alt);
    Serial.println (recieved_co[2].az);
    delay (5000);

    //Calulating the speed of az and alt (deg/ms)
    delta_co = calulate_delta (recieved_co[1], recieved_co[2]);
    Serial.print ("delta az = ");
    Serial.println (delta_co.az, 10);
    Serial.print ("delta alt = ");
    Serial.println (delta_co.alt, 10);
    delay (5000);
}