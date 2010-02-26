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

/**
 * mission_output
 * This structure is passed into and also returned from every
 * mission.  
 */
struct mission_output {

    // Cylindrical Coordinates
    float theta;  // Angle
    float phi;    //
    float rho;    // Speed

    // Depth
    //TODO
    float depth;

    IplImage* frame;
    bool mission_done;

};

/********* Mission Definitions **********/
// Mission Constants
#define MISSION_WAIT 0
#define MISSION_GATE 1 
#define MISSION_GATE_PATH 11
#define MISSION_BOUEY 3
#define MISSION_BOUEY_PATH 33
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
    [MISSION_BOUEY] = "BOUEY",
    [MISSION_BOUEY_PATH] = "BOUEY_PATH",
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

// Gives the order which the missions are executed
static const int mission_order[] = {
    MISSION_GATE,
    MISSION_GATE_PATH,
    MISSION_BOUEY,
    MISSION_BOUEY_PATH,
    MISSION_HEDGE,
    MISSION_HEDGE_PATH,
    MISSION_WINDOW,
    MISSION_WINDOW_PATH,
    MISSION_WEAPONS_RUN,
    MISSION_WEAPONS_RUN_PATH,
    MISSION_MACHETE,
    MISSION_BRIEFCASE_GRAB,
    MISSION_OCTOGON,
    MISSION_WAIT,
};

/*********** Mission Prototypes **************/
void mission_gate_init(IplImage* frame);
struct mission_output mission_gate_step(struct mission_output);

void mission_bouy_init(IplImage* frame);
struct mission_output mission_bouy_step(struct mission_output);

#endif
