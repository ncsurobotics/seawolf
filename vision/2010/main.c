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

    // Setup Initial results struct
    struct mission_output results;
    results.theta = 0;
    results.phi = 0;
    results.rho = 0;
    results.depth_control = 0;
    results.depth = 0;
    results.mission_done = false;
    struct mission_output previous_results = results;

    #ifdef VISION_SHOW_HEADING
       cvNamedWindow("Heading", CV_WINDOW_AUTOSIZE);
    #endif

    // Determino mission_index
    int mission_index;
    #ifdef VISION_INITIAL_MISSION
        mission_index = VISION_INITIAL_MISSION;
    #else
        mission_index = 0;
    #endif
    printf("Starting Mission: %s\n",
            mission_strings[mission_order[mission_index]]);
    
    for (unsigned int frame_num=0; true; frame_num++)
    {
        
        // State machine
        int current_mission = mission_order[mission_index];
        results.frame = NULL;
        results.mission_done = false;
        switch (current_mission) {
            
            case MISSION_GATE:
                results = mission_gate_step(results);
            break;

            case MISSION_GATE_PATH:
                //TODO
            break;

            case MISSION_BOUY:
                results = mission_bouy_step(results);
            break;
            
            case MISSION_BOUY_PATH:
                //TODO
            break;

            case MISSION_HEDGE:
                //TODO
            break;

            case MISSION_HEDGE_PATH:
                //TODO
            break;

            case MISSION_WINDOW:
                //TODO
            break;

            case MISSION_WINDOW_PATH:
                //TODO
            break;

            case MISSION_WEAPONS_RUN:
                //TODO
            break;

            case MISSION_WEAPONS_RUN_PATH:
                //TODO
            break;

            case MISSION_MACHETE:
                //TODO
            break;

            case MISSION_BRIEFCASE_GRAB:
                //TODO
            break;

            case MISSION_OCTOGON:
                //TODO
            break;

            case MISSION_WAIT:
                //TODO
            break;

            default:
                printf("Error: Invalid mission \"%d\"", current_mission);
                exit(1);
            break;
        }

        printf("Theta, Phi, Rho: %f, %f, %f\n", results.theta, results.phi, results.rho);

        // Give mission control its heading
        if (memcmp(&results, &previous_results, sizeof(struct mission_output))) {

            // Update Variables
            Var_set("SetPointVision.Theta", results.theta);
            Var_set("SetPointVision.Phi", results.phi);
            Var_set("SetPointVision.Rho", results.rho);
            Var_set("DepthHeading", results.depth);
            Var_set("TrackerDoDepth", results.depth_control);
            Notify_send("UPDATED", "SetPointVision");
            previous_results = results;

            // Switch missions
            if (results.mission_done) {
                results.mission_done = false;
                printf("Finished mission: ");
                printf("%s\n", mission_strings[current_mission]);
                mission_index++;
                printf("Starting mission: ");
                printf("%s\n", mission_strings[mission_order[mission_index]]);

                // Init Next Mission
                switch (current_mission) {

                    case MISSION_GATE:
                        results = mission_gate_step(results);
                    break;

                    case MISSION_GATE_PATH:
                        //TODO
                    break;

                    case MISSION_BOUY:
                        results = mission_bouy_step(results);
                    break;
                    
                    case MISSION_BOUY_PATH:
                        //TODO
                    break;

                    case MISSION_HEDGE:
                        //TODO
                    break;

                    case MISSION_HEDGE_PATH:
                        //TODO
                    break;

                    case MISSION_WINDOW:
                        //TODO
                    break;

                    case MISSION_WINDOW_PATH:
                        //TODO
                    break;

                    case MISSION_WEAPONS_RUN:
                        //TODO
                    break;

                    case MISSION_WEAPONS_RUN_PATH:
                        //TODO
                    break;

                    case MISSION_MACHETE:
                        //TODO
                    break;

                    case MISSION_BRIEFCASE_GRAB:
                        //TODO
                    break;

                    case MISSION_OCTOGON:
                        //TODO
                    break;

                    case MISSION_WAIT:
                        //TODO
                    break;

                    default:
                        printf("Error: Invalid mission \"%d\"", current_mission);
                        exit(1);
                    break;
                }

            }

        }

        #ifdef VISION_SHOW_HEADING
            // Heading Circle
            if (results.frame != NULL) {
                CvPoint heading = {results.theta + results.frame->width/2,
                                   results.phi + results.frame->height/2};
                cvCircle(results.frame, heading, 5, cvScalar(0,255,0,0),1,8,0);
                // Middle Circle
                cvCircle(results.frame, cvPoint(results.frame->width/2, results.frame->height/2), 5, cvScalar(0,255,255,0),1,8,0);
                cvShowImage("Heading", results.frame);
            }
        #endif

        // Handle Keys
        int key = cvWaitKey(DELAY);
        if ( (char) key == 27) { // Esc to exit
            break;
        }
        switch ( (char) key) {
            // Keyboard Commands
        }

    }

}
