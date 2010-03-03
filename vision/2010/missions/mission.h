//header for mission-related files 
#ifndef __SEAWOLF_VISION_MISSION_INCLUDE_H
#define ___SEAWOLF_VISION_MISSION_INCLUDE_H

#include <stdbool.h>
#include <highgui.h>
#include <opencv/cv.h>

// Misc Constants
#define MAX_THETA 100
#define MAX_PHI   20
#define MAX_RHO   50

#define DEPTH_RELATIVE 1.0
#define DEPTH_ABSOLUTE 0.0

/**
 * mission_output
 * This structure is passed into and also returned from every mission.  
 */
struct mission_output {

    // Cylindrical Coordinates
    float theta;  // Angle
    float rho;    // Speed

    // Depth
    // Control for depth is either absolute or relative.  If "depth_control" is
    // DEPTH_ABSOLUTE then the "depth" variable is used.  If "depth_control" is
    // DEPTH_RELATIVE then the "phi" variable is used.
    float depth_control;
    float depth;  // Absolute Depth
    float phi;    // Relative Depth

    // Missions should set this to the frame they recieved from the camera, so
    // main.c can use it for debugging.  Missions may also write debug
    // information on this image and it will be displayed.  
    IplImage* frame;

    // This flag is set to true inside a mission when the mission is completed.
    // main.c notices when this is set to true and switches to the next
    // mission.
    bool mission_done;

};

/********* Mission Definitions **********/
// Mission Constants
#define MISSION_WAIT 0
#define MISSION_GATE 1 
#define MISSION_GATE_PATH 11
#define MISSION_BOUY 3
#define MISSION_BOUY_PATH 33
#define MISSION_HEDGE 4
#define MISSION_HEDGE_PATH 44
#define MISSION_WINDOW 5
#define MISSION_WINDOW_PATH 55
#define MISSION_WEAPONS_RUN 6
#define MISSION_WEAPONS_RUN_PATH 66
#define MISSION_MACHETE 7
#define MISSION_BRIEFCASE_GRAB 77
#define MISSION_OCTOGON 8

static const char* mission_strings[] = {
    [MISSION_WAIT] = "WAIT",
    [MISSION_GATE] = "GATE",
    [MISSION_GATE_PATH] = "GATE_PATH",
    [MISSION_BOUY] = "BOUY",
    [MISSION_BOUY_PATH] = "BOUY_PATH",
    [MISSION_HEDGE] = "HEDGE",
    [MISSION_HEDGE_PATH] = "HEDGE_PATH",
    [MISSION_WINDOW] = "WINDOW",
    [MISSION_WINDOW_PATH] = "WINDOW_PATH",
    [MISSION_WEAPONS_RUN] = "WEAPONS_RUN",
    [MISSION_WEAPONS_RUN_PATH] = "WEAPONS_RUN_PATH",
    [MISSION_MACHETE] = "MACHETE",
    [MISSION_BRIEFCASE_GRAB] = "BRIEFCASE_GRAB",
    [MISSION_OCTOGON] = "OCTOGON",
};

// Gives the order which the missions are executed.  The initial mission
// defaults to 0, but can be changed in debug.mk
static const int mission_order[] = {
    MISSION_GATE,
    //MISSION_GATE_PATH,
    MISSION_BOUY,
    //MISSION_BOUY_PATH,
    MISSION_HEDGE,
    //MISSION_HEDGE_PATH,
    MISSION_WINDOW,
    //MISSION_WINDOW_PATH,
    MISSION_WEAPONS_RUN,
    //MISSION_WEAPONS_RUN_PATH,
    MISSION_MACHETE,
    MISSION_BRIEFCASE_GRAB,
    MISSION_OCTOGON,
    MISSION_WAIT,
};

/*********** Mission Prototypes **************/
// Gate
void mission_gate_init(IplImage* frame);
struct mission_output mission_gate_step(struct mission_output);

// Bouy
void mission_bouy_init(IplImage* frame);
struct mission_output mission_bouy_step(struct mission_output);

#endif
