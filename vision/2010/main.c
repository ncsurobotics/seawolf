#include <seawolf.h>

#define DELAY 10

#define MAX_THETA 100
#define MAX_PHI   20
#define MAX_RHO   50

int main(int argc, char** argv)
{
    
    // Seawolf Init
    Seawolf_loadConfig("../../conf/seawolf.conf");
    Seawolf_init("Vision Mission Control");

    // Set filter for seasql notify messages
    Notify_filter(FILTER_ACTION, "GO");

    float theta = 0;
    float phi = 0;
    float rho = 0;

//struct {
    //is_done
    //theta
    //phi
    //rho
//}

    while (1)
    {
        
        // State machine
        mission_gate_step(frame);
        //TODO

        // Give mission control its heading
        printf("Theta, Phi,Rho: %f, %f,%f\n", theta, phi,rho);
        SeaSQL_setSetPointVision_Theta(theta);
        SeaSQL_setSetPointVision_Phi(phi);
        SeaSQL_setSetPointVision_Rho(rho);
        Notify_send("UPDATED", "SetPointVision");

        cvWaitKey(DELAY);

    }

}
