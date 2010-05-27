
#include "seawolf.h"
#include "seawolf3.h"

#include <ncurses.h>
#include <pthread.h>
#include <math.h>

#define PORTY 0
#define STARY 1
#define AFT   2
#define PORTX 3
#define STARX 4

#define PORT 0
#define STAR 1

static int count;

#if 0

#define FRAC_ROLL 0.2
#define FRAC_PITCH 0.2
#define FRAC_DEPTH 0.6

#define FRAC_FORWARD 0.5
#define FRAC_YAW 0.5

/* Simple proportional mixing algorithm */
static void mix(short req_roll[2], short req_pitch[3], short req_depth[3], short req_forward[2], short req_yaw[2], short out[5]) {
    out[PORTY] = (req_roll[PORT] * FRAC_ROLL) + (req_pitch[PORT] * FRAC_PITCH) + (req_depth[PORT] * FRAC_DEPTH);
    out[STARY] = (req_roll[STAR] * FRAC_ROLL) + (req_pitch[STAR] * FRAC_PITCH) + (req_depth[STAR] * FRAC_DEPTH);
    out[AFT] = (req_pitch[AFT] * FRAC_PITCH) + (req_depth[AFT] * FRAC_DEPTH);
    out[PORTX] = (req_forward[PORT] * FRAC_FORWARD) + (req_yaw[PORT] * FRAC_YAW);
    out[STARX] = (req_forward[STAR] * FRAC_FORWARD) + (req_yaw[STAR] * FRAC_YAW);
}

#else

/* Simple summing mixing algorithm */
static void mix(short req_roll[2], short req_pitch[3], short req_depth[3], short req_forward[2], short req_yaw[2], short out[5]) {
    out[PORTY] = req_roll[PORT] + req_pitch[PORT] + req_depth[PORT];
    out[STARY] = req_roll[STAR] + req_pitch[STAR] + req_depth[STAR];
    out[AFT] = req_pitch[AFT] + req_depth[AFT];
    out[PORTX] = req_forward[PORT] + req_yaw[PORT];
    out[STARX] = req_forward[STAR] + req_yaw[STAR];
}

#endif // #if 0

static void setThrusters(short out[5]) {
    /* Set all thurster values */
    Var_set("PortY", out[PORTY]);
    Var_set("StarY", out[STARY]);
    Var_set("Aft", out[AFT]);

    Var_set("PortX", out[PORTX]);
    Var_set("StarX", out[STARX]);
}

static int rate(void) {
    Timer* t = Timer_new();

    while(true) {
        Logging_log(DEBUG, Util_format("%.2f updates/sec", count / Timer_getDelta(t)));
        count = 0;

        Util_usleep(2);
    }

    return 0;
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("PID Mixer");

    Var_set("DepthHeading", 0.5);

    /* Thruster values */
    short out[] = {0, 0, 0, 0, 0};
    
    /* Value requests from PID's */
    short req_roll[]    = {0, 0};    /* port_y, star_y */
    short req_pitch[]   = {0, 0, 0}; /* port_y, star_y, aft */
    short req_depth[]   = {0, 0, 0}; /* port_y, star_y, aft */
    short req_forward[] = {0, 0};    /* port_x, star_x */
    short req_yaw[]     = {0, 0};    /* port_x, star_x */

    /* Notify buffers */
    char action[32], data[64];
    char requester[16], values[48];

    /* Zero thrusters */
    setThrusters(out);

    /* Notify filters */
    Notify_filter(FILTER_ACTION, "THRUSTER_REQUEST");
    
    count = 0;
    Task_background(rate);

    while(true) {
        Notify_get(action, data);
        Util_split(data, ' ', requester, values);

        count++;

        /* Parse request */
        if(strcmp(requester, "Roll") == 0) {
            sscanf(values, "%hd%hd", &req_roll[PORT], &req_roll[STAR]);
        } else if(strcmp(requester, "Yaw") == 0) {
            sscanf(values, "%hd%hd", &req_yaw[PORT], &req_yaw[STAR]);
        } else if(strcmp(requester, "Forward") == 0) {
            sscanf(values, "%hd%hd", &req_forward[PORT], &req_forward[STAR]);
        } else if(strcmp(requester, "Pitch") == 0) {
            sscanf(values, "%hd%hd%hd", &req_pitch[PORT], &req_pitch[STAR], &req_pitch[AFT]);
        } else if(strcmp(requester, "Depth") == 0) {
            sscanf(values, "%hd%hd%hd", &req_depth[PORT], &req_depth[STAR], &req_depth[AFT]);
        } else {
            continue;
        }

        /* Mix */
        mix(req_roll, req_pitch, req_depth, req_forward, req_yaw, out);

        /* Check bounds on all output values */
        out[PORTY] = Util_inRange(-THRUSTER_MAX, out[PORTY], THRUSTER_MAX);
        out[STARY] = Util_inRange(-THRUSTER_MAX, out[STARY], THRUSTER_MAX);
        out[AFT]   = Util_inRange(-THRUSTER_MAX, out[AFT]  , THRUSTER_MAX);
        out[PORTX] = Util_inRange(-THRUSTER_MAX, out[PORTX], THRUSTER_MAX);
        out[STARX] = Util_inRange(-THRUSTER_MAX, out[STARX], THRUSTER_MAX);

        /* Output new thruster values */
        setThrusters(out);
    }

    Seawolf_close();
    return 0;
}
