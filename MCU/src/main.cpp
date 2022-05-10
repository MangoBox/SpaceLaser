#include<Arduino.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include <iostream>
#include <cstdlib>
//Motor thingo 
#include <AccelStepper.h>
//Our header files
#include <Variables.h>
#include <Functions.h>


void setup(){
    // Local variables
    int wait_period = 306000; // 5 mins
    int baud_rate = 9600;

    //Starting serial
    Serial.begin(baud_rate);
    Serial.setTimeout (wait_period);
}

void loop(){
    //Local variables
    struct horizon_co current_co, delta_co ;
    
    /****************************************************
     * Recieving Data from computer
    ****************************************************/
    // START WITH A WHILE AND THEN MOVE TO IF MAYBE
    //timer interput EXAMPLE IS BLINK WITHOUT DELAY SERIAL WITHOUT WAITING
    // LOOK UP SERIAL INERUPT
    while(Serial.available() == 0){
    }
    
    // Recieving number of data sets being sent and time interval (ms)
    //NUM_DATAPT = Serial.readStringUntil (',').toInt();
    //T_interval = Serial.readStringUntil ('\r').toInt();

    //ERROR CHECK USING REGEX. First save as string and pattern match.

    //Delcaring main data storage variable
    struct horizon_co recieved_co [NUM_DATAPT];

    // Extracting data
    String Raw_Data_S;
    char Raw_Data [55];
    for (int i = 0; i < NUM_DATAPT; i ++){
        Raw_Data_S = Serial.readStringUntil('\r');
        //delay (30);
        Serial.print ("raw data = ");
        Serial.println (Raw_Data_S);
        // Do a REGEX check here
        Raw_Data_S.toCharArray(Raw_Data, 55);
        recieved_co[i] = String_strtok (Raw_Data, Strtok_outputs);  
        Serial.print ("az / alt = ");
        Serial.print (recieved_co[i].az);
        Serial.print(", ");
        Serial.println(recieved_co[i].alt);
    }
    /****************************************************
     * TESTING WITH HARD CODED DATA
    ****************************************************/
    if (Using_hardcode){
        char Raw_Data_1[55] = "133.193231,-27.095697,2022-04-29,22:07:06";
        char Raw_Data_2[55] = "180.123433,-95.900123,2022-04-29,22:07:11";

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
}