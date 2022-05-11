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

    //Set max turning speeds
    stepper1.setMaxSpeed(40.0);
    stepper2.setMaxSpeed(40.0);

    //Set accelerations
    stepper1.setAcceleration(20.0);
    stepper2.setAcceleration(20.0);
}

void loop(){
    //Local variables
    struct horizon_co current_co, delta_co ;
    //Delcaring main data storage variable
    struct horizon_co recieved_co [NUM_DATAPT];
    //case variables
    char key = 'z';
    String Raw_Data_S;
    char Raw_Data [55];
    // Find how to make i only run once here
    
    /*****************************************************************
     * Recieving Data from computer
    *****************************************************************/
    // START WITH A WHILE AND THEN MOVE TO IF MAYBE
    //timer interput EXAMPLE IS BLINK WITHOUT DELAY SERIAL WITHOUT WAITING
    // LOOK UP SERIAL INERUPT

    while(Serial.available() == 0){
    }

    key = Serial.read();

    switch (key){
        //Getting date / time / time interval
        case 'a': Initialisation (); 
            i = 0;
            break;
        
        // Extracting data new data
        case 'b': Raw_Data_S = Serial.readStringUntil('\r');
            Raw_Data_S.toCharArray(Raw_Data, 55);
            recieved_co[i] = String_strtok (Raw_Data, Strtok_outputs); 
            i ++;
            break;
        
        default: 
            break;
    }


    //ERROR CHECK USING REGEX. First save as string and pattern match.

    
    /*****************************************************************
     * TESTING WITH HARD CODED DATA
    *****************************************************************/
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

        //Change Direction at limits
        if(stepper1.distanceToGo() == 0)
            stepper1.moveTo(-stepper1.CurrentPostion);
        if(stepper2.distanceToGo() == 0)
            stepper2.moveTo(-stepper1.CurrentPostion);
        
        //Stepper movement altitude
        stepper1.moveTo(recieved_co[1].alt)
        while (stepper1.currentPosition() != (recieved_co[1]-50)||(recieved_co+50))
            stepper1.run();
        stepper1.stop();
        stepper1.runToPostion();
        stepper1.moveTo(recieved_co[1].alt);

        //Stepper movement azimuth
        while (stepper2.currentPosition() != (recieved_co[1]-50)||(recieved_co+50))
            stepper2.run();
        stepper2.stop();
        stepper2.runToPostion();
        stepper2.moveTo(recieved_co[1].az);

    }
}