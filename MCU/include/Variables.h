/*****************************************************************
GLOBAL VARIABLES:
*****************************************************************/
//Number of data points we are reciving
int NUM_DATAPT = 20;
// Time interval between data points in ms
int T_interval = 6000;  //Hard coded for 5 minutes

//Print String_Strtok function outputs??
const bool Strtok_outputs = false;

//Main data type
struct horizon_co {
    double az;
    double alt;
    String date;
    String time;
};
