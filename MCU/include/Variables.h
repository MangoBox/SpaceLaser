/*****************************************************************
GLOBAL VARIABLES:
*****************************************************************/
//Number of data points we are reciving
int NUM_DATAPT = 1;
// Time interval between data points in ms
int T_interval = 6000;  //Hard coded for 5 minutes
// Date and time at start of recieving data
String CURRENT_DATE;
// current data point being read
int i = 0;

//Print String_Strtok function outputs??
const bool Strtok_outputs = true;
const bool Using_hardcode = false;

//Defining main data type
struct horizon_co {
    double az;
    double alt;
    String date;
    String time;
};
