
#include "seawolf.h"
#include "seawolf3.h"

#include <ncurses.h>
#include <pthread.h>
#include <math.h>

#define PORTX  0
#define STARX  1
#define STRAFE 2
#define BOW    3
#define FORE   4

#define PORT 0
#define STAR 1

static int count;

#if 0

#define FRAC_PITCH 0.35
#define FRAC_DEPTH 0.65

#define FRAC_FORWARD 0.5
#define FRAC_YAW 0.5

/* Simple proportional mixing algorithm */
static void mix(short req_pitch[3], short req_depth[3], short req_forward[2], short req_yaw[2], short req_strafe, short out[5]) {
    out[BOW] = (req_pitch[0] * FRAC_PITCH) + (req_depth[0] * FRAC_DEPTH);
    out[FORE] = (req_pitch[1] * FRAC_PITCH) + (req_depth[1] * FRAC_DEPTH);
    out[PORTX] = (req_forward[0] * FRAC_FORWARD) + (req_yaw[0] * FRAC_YAW);
    out[STARX] = (req_forward[1] * FRAC_FORWARD) + (req_yaw[1] * FRAC_YAW);
    out[STRAFE] = req_strafe;
}

#else

/* Simple summing mixing algorithm */
static void mix(short req_pitch[2], short req_depth[2], short req_forward[2], short req_yaw[2], short req_strafe, short out[5]) {
    out[BOW] = req_pitch[0] + req_depth[0];
    out[FORE] = req_pitch[1] + req_depth[1];
    out[PORTX] = req_forward[0] + req_yaw[0];
    out[STARX] = req_forward[1] + req_yaw[1];
    out[STRAFE] = req_strafe;
}

#endif // #if 0

static void setThrusters(short out[5]) {
    /* Set all thurster values */
    Var_set("Bow", out[BOW]);
    Var_set("Fore", out[FORE]);
    Var_set("PortX", out[PORTX]);
    Var_set("StarX", out[STARX]);
    Var_set("Strafe", out[STRAFE]);
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

    /* Thruster values */
    short out[] = {0, 0, 0, 0, 0};
    
    /* Value requests from PID's */
    short req_strafe    = 0;
    short req_pitch[]   = {0, 0}; /* bow, fore */
    short req_depth[]   = {0, 0}; /* bow, fore */
    short req_forward[] = {0, 0}; /* port_x, star_x */
    short req_yaw[]     = {0, 0}; /* port_x, star_x */

    /* Notify buffers */
    char data[64];
    char requester[16], values[48];

    /* Zero thrusters */
    setThrusters(out);

    /* Notify filters */
    Notify_filter(FILTER_ACTION, "THRUSTER_REQUEST");
    
    count = 0;
    Task_background(rate);

    Notify_send("GO", "Vision");

    while(true) {
        Notify_get(NULL, data);
        Util_split(data, ' ', requester, values);

        count++;

        /* Parse request */
        if(strcmp(requester, "Yaw") == 0) {
            sscanf(values, "%hd%hd", &req_yaw[0], &req_yaw[1]);
        } else if(strcmp(requester, "Forward") == 0) {
            sscanf(values, "%hd%hd", &req_forward[0], &req_forward[1]);
        } else if(strcmp(requester, "Pitch") == 0) {
            sscanf(values, "%hd%hd", &req_pitch[0], &req_pitch[1]);
        } else if(strcmp(requester, "Depth") == 0) {
            sscanf(values, "%hd%hd", &req_depth[0], &req_depth[1]);
        } else if(strcmp(requester, "Strafe") == 0) {
            sscanf(values, "%hd", &req_strafe);
        } else {
            continue;
        }

        /* Mix */
        mix(req_pitch, req_depth, req_forward, req_yaw, req_strafe, out);

        /* Check bounds on all output values */
        out[BOW]    = Util_inRange(-THRUSTER_MAX, out[BOW], THRUSTER_MAX);
        out[FORE]   = Util_inRange(-THRUSTER_MAX, out[FORE], THRUSTER_MAX);
        out[STRAFE] = Util_inRange(-THRUSTER_MAX, out[STRAFE], THRUSTER_MAX);
        out[PORTX]  = Util_inRange(-THRUSTER_MAX, out[PORTX], THRUSTER_MAX);
        out[STARX]  = Util_inRange(-THRUSTER_MAX, out[STARX], THRUSTER_MAX);

        /* Output new thruster values */
        setThrusters(out);
    }

    Seawolf_close();
    return 0;
}
