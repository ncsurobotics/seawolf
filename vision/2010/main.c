#include <seawolf.h>
#include <seawolf3.h>

#include "vision_lib.h"
#include "missions/mission.h"
#include "control.h"

#define DELAY 10

#define MAX_THETA 100
#define MAX_PHI   20
#define MAX_RHO   50

// Prototypes
void mission_init(int current_mission, IplImage* frame);
struct mission_output* mission_step(struct mission_output* results, int mission);

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
    results.yaw_control = ROT_MODE_ANGULAR;
    results.yaw = 0;
    results.rho = 0;
    results.depth_control = 0;
    results.depth = 0;
    results.mission_done = false;
    struct mission_output previous_results = results;

    #ifdef VISION_SHOW_HEADING
       cvNamedWindow("Heading", CV_WINDOW_AUTOSIZE);
    #endif

    // Determine mission_index
    int mission_index;
    #ifdef VISION_INITIAL_MISSION
        mission_index = VISION_INITIAL_MISSION;
    #else
        mission_index = 0;
    #endif
    results.frame = multicam_get_frame(FORWARD_CAM);
    mission_init(mission_order[mission_index], results.frame);

    for (unsigned int frame_num=0; true; frame_num++)
    {

        // Run mission_step
        int current_mission = mission_order[mission_index];
        results.frame = NULL;
        results.mission_done = false;
        results = *mission_step(&results, current_mission);
        printf("Theta, Phi, Rho: %f, %f, %f\n", results.yaw, results.depth, results.rho);

        // Give mission control its heading
        if (memcmp(&results, &previous_results, sizeof(struct mission_output))) {

            // Set headings
            set_depth(results.depth, results.depth_control);
            set_yaw(results.yaw, results.yaw_control);
            previous_results = results;

            // Switch missions
            if (results.mission_done) {
                results.mission_done = false;
                printf("Finished mission: %s\n",
                        mission_strings[current_mission]);
                mission_index++;
                current_mission = mission_order[mission_index];
                mission_init(current_mission, results.frame);

            }

        }

        #ifdef VISION_SHOW_HEADING
            // Heading Circle
            if (results.frame != NULL) {
                CvPoint heading = {results.yaw + results.frame->width/2,
                                   results.depth + results.frame->height/2};
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

            // Pause
            case ' ':
                printf("Paused.  Press space bar to unpause.\n");
                while (true) {
                    key = cvWaitKey(100);
                    if (key == 27) exit(0);
                    if (key == ' ') break;
                }
            break;

        }

    }

}

void mission_init(int current_mission, IplImage* frame)
{
    printf("Starting Mission: %s\n", mission_strings[current_mission]);
    switch (current_mission) {

        case MISSION_GATE:
            mission_gate_init(frame, 1.0);
        break;

        case MISSION_ALIGN_PATH:
            mission_align_path_init(frame);
        break;

        case MISSION_BOUY:
            mission_bouy_init(frame);
        break;

        case MISSION_HEDGE:
            mission_gate_init(frame, 2.0);
        break;

        case MISSION_WINDOW:
            //TODO
        break;

        case MISSION_WEAPONS_RUN:
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

        case MISSION_STOP:
        break;

        default:
            printf("Error: Invalid mission \"%d\"", current_mission);
            exit(1);
        break;

    }
}

struct mission_output* mission_step(struct mission_output* results, int mission)
{
    switch (mission) {

        case MISSION_GATE:
            *results = mission_gate_step(*results);
        break;

        case MISSION_ALIGN_PATH:
            *results = mission_align_path_step(*results);
        break;

        case MISSION_BOUY:
            *results = mission_bouy_step(*results);
        break;

        case MISSION_HEDGE:
            *results = mission_gate_step(*results);
        break;

        case MISSION_WINDOW:
            //TODO
        break;

        case MISSION_WEAPONS_RUN:
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

        case MISSION_STOP:
            Util_usleep(1);
            results->yaw = 0;
            results->depth = 0;
            results->rho = 0;
            results->depth_control = DEPTH_ABSOLUTE;
            results->depth = 0;
        break;

        default:
            printf("Error: Invalid mission \"%d\"", mission);
            exit(1);
        break;
    }

    return results;
}
