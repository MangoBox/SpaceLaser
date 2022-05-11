#include<Arduino.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include <iostream>
#include <cstdlib>
#include <arduino-timer.h>
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
    struct horizon_co delta_co ;
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
    //ERROR CHECK USING REGEX. First save as string and pattern match.

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
    
    
/*****************************************************************
 * MOTOR FUNCTIONS
*****************************************************************/
    // Checking time 
    timer.tick();
    //Change Direction at limits
    if(stepper1.distanceToGo() == 0)
        stepper1.moveTo(-stepper1.currentPosition());
    if(stepper2.distanceToGo() == 0)
        stepper2.moveTo(-stepper2.currentPosition());
    
    //Stepper movement altitude
    stepper1.moveTo(recieved_co[next_co].alt);
    while (stepper1.currentPosition() != (recieved_co[next_co].alt-50)||(recieved_co[next_co].alt +50))
        stepper1.run();
    stepper1.stop();
    stepper1.runToPosition();

    //Stepper movement azimuth
    stepper2.moveTo(recieved_co[next_co].az);
    while (stepper2.currentPosition() != (recieved_co[next_co].az-50)||(recieved_co[next_co].az+50))
        stepper2.run();
    stepper2.stop();
    stepper2.runToPosition();
}