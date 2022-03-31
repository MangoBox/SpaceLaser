#include<stdio.h>

struct horizon_co {
double az;
double alt;
};

/*****************************************************************
GLOBAL VARIABLES:
*****************************************************************/

/*****************************************************************
FUNCTION DECLARATION
*****************************************************************/
/*Function to calculate delta co*/
horizon_co calulate_delta (horizon_co, horizon_co);


int main(void){
    /*Local variables*/
    struct horizon_co recieved_co [30], current_co, delta_co ;
    
    delta_co = calulate_delta (current_co, recieved_co[0]);
}

/*****************************************************************
FUNCTIONS
*****************************************************************/

horizon_co calulate_delta(horizon_co current_co, horizon_co future_co){
/*Local variable*/
horizon_co delta_co;
/*Function*/
delta_co.alt = future_co.alt - current_co.alt;
delta_co.az = future_co.az - current_co.az;
return delta_co;
};
