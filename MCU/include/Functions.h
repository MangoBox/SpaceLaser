
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
    const float Step = 0.2;
    for (int i = 0; i < NUM_DATAPT; i++){
        SCoor[i].alt = DCoor[i].alt / Step;
        SCoor[i].az = DCoor[i].az / Step;
    }
};

// String extraction function
horizon_co String_strtok (char input_string[], bool print_outputs){

    //Variables
    horizon_co extracted_data;
    char * token;

    // Extract Azimuth
    token = strtok(input_string, ",");
    extracted_data.az = std :: atof (token);
    
    if (print_outputs){
        Serial.print ("az token = ");
        Serial.println (token);
        Serial.print ("az output = ");
        Serial.println (extracted_data.az, 6);
        Serial.println (); 
    }

    //Extracting Altitude
    token = strtok(NULL, ",");
    extracted_data.alt = std :: atof (token);

    if (print_outputs){
        Serial.print ("alt token = ");
        Serial.println (token);
        Serial.print ("alt output = ");
        Serial.println (extracted_data.alt, 6);
        Serial.println (); 
    }

    //Extracting Date
    token = strtok(NULL, ",");
    extracted_data.date = token;

    if (print_outputs){
        Serial.print ("Date token = ");
        Serial.println (token);
        Serial.print ("Date output = ");
        Serial.println (extracted_data.date);
        Serial.println (); 
    }

    //Extracting Time
    token = strtok(NULL, ",");
    extracted_data.time = token;

    if (print_outputs){
        Serial.print ("time token = ");
        Serial.println (token);
        Serial.print ("time output = ");
        Serial.println (extracted_data.time);
        Serial.println (); 
    }

    return extracted_data;
}

//Format check for recieved data
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