#include<Arduino.h>
#include<stdio.h>

/*****************************************************************
FUNCTIONS
*****************************************************************/

//Calculating the difference between horizon coordinates
horizon_co calulate_delta(horizon_co current_co, horizon_co future_co){
    /*Local variable*/
    horizon_co delta_co;
    /*Function*/
    delta_co.alt = future_co.alt - current_co.alt;
    delta_co.az = future_co.az - current_co.az;
    return delta_co;
};

//Degrees to motor steps
void Deg_to_Step (horizon_co DCoor[], horizon_co SCoor[]){
    float Step = 0.2;
    for (int i = 0; i < NUM_DATAPT; i++){
        SCoor[i].alt = DCoor[i].alt / Step;
        SCoor[i].az = DCoor[i].az / Step;   
    }
};



/*****************************************************************
FUNCTIONS WE NEED TO BUILD:
Caclculating Acceleration
Calc Deceleration?
Current velocity
Communication x 7
Calc Current pos
Defining path
Protection for motors and laser.
*****************************************************************/