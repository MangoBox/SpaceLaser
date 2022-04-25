#include<Arduino.h>
#include<stdio.h>
#include<string.h>

/*****************************************************************
FUNCTIONS
*****************************************************************/

//Calculating the difference between horizon coordinates
horizon_co calulate_delta(horizon_co current_co, horizon_co future_co){
    /*Local variable*/
    horizon_co delta_co;
    /*Function*/
    delta_co.alt = (future_co.alt - current_co.alt) / T_interval;
    delta_co.az = (future_co.az - current_co.az) / T_interval;
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

// String token 
void String_strtok (void){
   // Place holder for the data we will recieve
   char input_string[400] = "123123,123123123,123712837128937";

   // Extract the first token
   char * token = strtok(input_string, ",");
   // loop through the string to extract all other tokens
   while( token != NULL ) {
      printf( " %s", token ); //printing each token
      token = strtok(NULL, ",");
   }
   return;
}

//format check for recieved data
int format_check (){

}




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