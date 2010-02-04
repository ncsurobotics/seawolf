//header for mission-related files 
#ifndef __SEAWOLF_VISION_MISSION_INCLUDE_H
#define ___SEAWOLF_VISION_MISSION_INCLUDE_H

#include <stdbool.h>
#include <highgui.h>
#include <opencv/cv.h>

struct mission_output {

    // Cylindrical Coordinates
    float theta;
    float phi;
    float rho;

    // Depth
    //TODO
    float depth;

    bool mission_done;

};

//TODO: Define missions for this year
#define WAIT 0
//EACH REAL MISSION INCLUDES FINDING THE NEXT APPROPRIATE MARKER (SINCE THAT IS SPECIFIC TO EACH MISSION) THEN ALLIGN_PATH ALLIGNS US WITH THAT MARKER
#define GATE 1 
#define GATE_PATH 11
#define BOUEY 3
#define BOUEY_PATH 33
#define BARBED_WIRE 4
#define BARBED_WIRE_ALLIGN 42
#define BARBED_WIRE_PATH 44
#define TORPEDO 5
#define TORPEDO_PATH 55
#define BOMBING_RUN 6
#define BOMBING_RUN_PATH 66
#define BOMBING_RUN_2 61
#define BOMBING_RUN_2_PATH 661
#define BRIEFCASE 7
#define BRIEFCASE_GRAB 77
#define OCTOGON 8
#define ALLIGN_PATH 9 //CALLED AFTER FINDING THE CORRECT PATH AFTER EACH MISSION, ONCE COMPLETED, RETURN RETURN TASK COMPLETE
#define IDENTIFY_SILHOUET 10
#define TUNA_BLOB 12
#define MOTION 13


#define MAX_THETA 100
#define MAX_PHI   20
#define MAX_RHO   50

//PROTOTYPES OF MISSION FUNCTIONS
void mission_gate_init(IplImage* frame);
struct mission_output mission_gate_step(struct mission_output);

#endif
