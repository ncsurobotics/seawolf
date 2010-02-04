#include <seawolf.h>
#include "vision_lib.h"
#include "missions/mission.h"

#define DELAY 10

#define MAX_THETA 100
#define MAX_PHI   20
#define MAX_RHO   50

int main(int argc, char** argv)
{
    
    // Seawolf Init
    Seawolf_loadConfig("../../conf/seawolf.conf");
    Seawolf_init("Vision Mission Control");

    // Setup Cameras
    if (argc == 4) {
        multicam_set_camera(DOWN_CAM, argv[1]);
        multicam_set_camera(FORWARD_CAM, argv[2]);
        multicam_set_camera(UP_CAM, argv[3]);
    } else if (argc == 3) {
        multicam_set_camera(DOWN_CAM, argv[1]);
        multicam_set_camera(FORWARD_CAM, argv[2]);
        multicam_set_camera(UP_CAM, argv[1]);
    } else if (argc == 2) {
        multicam_set_camera(DOWN_CAM, argv[1]);
        multicam_set_camera(FORWARD_CAM, argv[1]);
        multicam_set_camera(UP_CAM, argv[1]);
    } else {
        multicam_set_camera(DOWN_CAM, "0");
        multicam_set_camera(FORWARD_CAM, "0");
        multicam_set_camera(UP_CAM, "0");
    }

    // Set filter for seasql notify messages
    Notify_filter(FILTER_ACTION, "GO");

    struct mission_output results = {0,0,0,0,false};
    struct mission_output previous_results = results;

    while (1)
    {
        
        // State machine
        results = mission_gate_step(results);
        //TODO

        // Give mission control its heading
        //TODO: Depth
        if (memcmp(&results, &previous_results, sizeof(struct mission_output))) {
            printf("Theta, Phi, Rho: %f, %f, %f\n", results.theta, results.phi, results.rho);
            SeaSQL_setSetPointVision_Theta(results.theta);
            SeaSQL_setSetPointVision_Phi(results.phi);
            SeaSQL_setSetPointVision_Rho(results.rho);
            Notify_send("UPDATED", "SetPointVision");
            previous_results = results;
        }

        cvWaitKey(DELAY);

    }

}
