#include<Arduino.h>
#include<stdio.h>
#include <Variables.h>
#include <Functions.h>


/*****************************************************************
MAIN
*****************************************************************/
void setup(){

}

void loop(){
    /*Local variables*/
    struct horizon_co recieved_co [NUM_DATAPT];
    struct horizon_co current_co, delta_co ;
    
    delta_co = calulate_delta (current_co, recieved_co[0]);
}