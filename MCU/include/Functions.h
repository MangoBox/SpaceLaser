
/*****************************************************************
FUNCTIONS
*****************************************************************/
/*****************************************************************
FUNCTIONS WE NEED TO BUILD:
Current velocity
Calc Current pos
Defining path
Protection for motors and laser.
*****************************************************************/


/*****************************************************************
MOTOR FUNCTIONS
*****************************************************************/
// What position are we moving to?
bool update_pos(void *){
    next_co ++;
    return true;
}

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


/*****************************************************************
COMMUNICATION FUNCTIONS
*****************************************************************/
// Initialisation
void Initialisation (void){
    //getting interval
    String T_interval_S = Serial.readStringUntil (',');
    char T_interval_CA[20];
    T_interval_S.toCharArray(T_interval_CA, 20);
    T_interval = std :: atoi (T_interval_CA);
    timer.every (T_interval, update_pos);
    //getting current date
    CURRENT_DATE = Serial.readStringUntil (',');
    Serial.println ("interval = " + T_interval_S + "\nCurrent date = " + CURRENT_DATE);
}

// String extraction function
horizon_co String_strtok (char input_string[], bool print_outputs){

    //Variables
    horizon_co extracted_data;
    char * token;

    // Extract Azimuth
    token = strtok(input_string, ",");
    extracted_data.az = std :: atof (token);
    
    //Extracting Altitude
    token = strtok(NULL, ",");
    extracted_data.alt = std :: atof (token);

    //Extracting Date
    token = strtok(NULL, ",");
    extracted_data.date = token;

    //Extracting Time
    token = strtok(NULL, ",");
    extracted_data.time = token;

    //sending extracted data back to main program
    if (print_outputs){
        Serial.print ("az output = ");
        Serial.println (extracted_data.az, 6);
        Serial.println (); 

        Serial.print ("alt output = ");
        Serial.println (extracted_data.alt, 6);
        Serial.println (); 

        Serial.print ("Date output = ");
        Serial.println (extracted_data.date);
        Serial.println (); 

        Serial.print ("time output = ");
        Serial.println (extracted_data.time);
        Serial.println (); 
    }

    return extracted_data;
}

//Format check for recieved data USING REGEX
/*int format_check (){

}*/