#include <seawolf.h>
#include "vision.h"

int mission_state = GATE;

// This is a non blocking call that is called every time a mission is done
// It first gives seawolf the mission done signal, then checks to see if the
// go command is given back.
// Returns the next mission number

void wait_for_go()
{
    #ifndef debug_skip_go_wait
        Notify_get(NULL, NULL);
    #endif
}

int mission_done()
{

    char* mission_string;
    // Change state to the next mission
    switch (mission_state)
    {

        case GATE:
            mission_string = "GATE";
            mission_state = BOUEY;
        break;

        case BOUEY:
            mission_string = "BOUEY";
            mission_state = BARBED_WIRE;
        break;

        case BARBED_WIRE:
            mission_string = "BARBED_WIRE";
            mission_state = TORPEDO;
        break;

        case TORPEDO:
            mission_string = "TORPEDO";
            mission_state = BOMBING_RUN;
        break;

        case BOMBING_RUN:
            mission_string = "BOMBING_RUN";
            mission_state = BRIEFCASE;
        break;

        case BRIEFCASE:
            mission_string = "BRIEFCASE";
            mission_state = OCTOGON;
        break;

        case OCTOGON:
            mission_string = "OCTOGON";
            mission_state = WAIT;
        break;

        default:
            mission_string = "UNKNOWN";
        break;

    }
    // Give seawolf the mission done signal
    printf("Finished Mission: %s\n", mission_string);
    fflush(NULL);
    Notify_send("DONE", mission_string);
    // Wait until seasql gives us the mission go message
    #ifndef debug_skip_go_wait
        Notify_get(NULL, NULL);
    #endif

    return mission_state;

}
