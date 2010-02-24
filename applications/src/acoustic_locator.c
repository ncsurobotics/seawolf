
#include "seawolf.h"

#include <stdio.h>
#include <stdlib.h>

/* Find that pinger!
 *
 * Acoustics Pinger Locator
 *
 * Center Hydrophones 
 */

#define FOUND 1
#define NOT_FOUND 0 
#define _ERROR ((0.66667) / SPEED_OF_SOUND) //determines the delay at 180 degrees
#define TURN_LEFT 1
#define SPEED_OF_SOUND (1497 * 3.2808399)

int main(void) { return 0; }

#if 0
int main(){
    Seawolf_loadConfig("../../conf/seawolf.conf");
    Seawolf_init("Acoustics Location");
	
    char action[64], data[64];
    float delay[2];
    int mode = NOT_FOUND;
    double mv;
    PID* pid;
    
    pid = PID_new(0,
                  Var_get("AcousticsPID.p"),
                  Var_get("AcousticsPID.i"),
                  SeaSQL_AcousticsPID_d());		
    
    while(1){
        getDelay(delay);
        //send SeaWolf looking for the pinger
        PID_setSetPoint(pid, 0);
	
        /*	
         *	If we are, we head for the pinger, if not, we start searching.
         *	This portion of the code checks to see if we're inside our error.
         */
	
        if(delay[0] < _ERROR){
            if(delay[1] > 0){
                //update PID
                mv = PID_update(PID, delay[0]);
                mode = FOUND;
            }
            else{
                //offset the setpoint of the PID so we don't get stuck going the wrong direction
                PID_setSetPoint(pid, TURN_LEFT);
                //update PID
                mv = PID_update(PID, delay[0]);
                mode = NOT_FOUND;
            }
        }
        else{
            if(delay[1] < 0)
                delay[0] = -delay[0]; //if facing away from the pinger this gives us the shortest path
            //update PID
            mv = PID_update(pid, delay[0]);
            mode = NOT_FOUND;
        }
	
        DataOut(mv,);
	
    }
    
    return 1;
    
}

int getDelay(float* delay){
    //Gets the delays from SeaSQL
    char notifyAction[64], notifyMessage[64];
    Notify_filter (FILTER_MATCH, "UPDATED Accoustics");
    Notify_get(notifyAction, notifyMessage);
    
    delay* = SeaSQL_getDelay12;
    (delay + 1)* = SeaSQL_getDelay34;
    
    return 0
        }

void dataOut(double mv,int mode) {
    float port, starboard
	int thrust
	
        int port  = Util_inRange(-THRUSTER_MAX, (int) mv, THRUSTER_MAX);
    int starboard = -port
	
	//if the ping is "found" then start moving forward
	if(mode = FOUND){
            port +=10;
            starboard +=10;
	}
    Notify_send("THRUSTER_REQUEST", Util_format("Yaw %d %d", port, starboard));
}
#endif // #if 0
