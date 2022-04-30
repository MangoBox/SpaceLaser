
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
void String_strtok (char input_string[], horizon_co extracted_data){

   // Extract the first token
   char * token = strtok(input_string, ",");
   extracted_data.az = std :: atof (token);
   Serial.println (token);
   Serial.println (extracted_data.az);
   
   // loop through the string to extract all other tokens
   /*
   while( token != NULL ) {
      Serial.println (token); //printing each token
      token = strtok(NULL, ",");
   }
   */
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