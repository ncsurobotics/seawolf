
#include "seawolf.h"
#include "seawolf3.h"

#include <ncurses.h>
#include <pthread.h>
#include <math.h>

#define PORT   0
#define STAR   1
#define STRAFE 2
#define BOW    3
#define STERN  4

/* Trim port/star values to compensate for rotation from strafing */
#define STRAFE_TRIM 0.3

/* Trim bow/stern values to compensate for pitch from diving/surfacing */
#define PITCH_TRIM 0.1

#define UPDATE_TOLERANCE 0.01

/* Simple summing mixing algorithm */
static void mix(float req_pitch, float req_depth, float req_forward, float req_yaw, float req_strafe, float out[5]) {
    out[BOW] = req_pitch + req_depth;
    out[STERN] = -req_pitch + req_depth;
    out[PORT] = req_forward + req_yaw;
    out[STAR] = req_forward - req_yaw;
    out[STRAFE] = req_strafe;

    /* Trim port/starboad thrusters */
    if(out[STRAFE] != 0) {
        out[PORT] -= out[STRAFE] * STRAFE_TRIM;
        out[STAR] += out[STRAFE] * STRAFE_TRIM;
    }

    /* Trim bow/stern thrusters */
    if(req_depth != 0) {
        out[STERN] -= req_depth * PITCH_TRIM;
        out[BOW] += req_depth * PITCH_TRIM;
    }
}

static void setThrusters(float out[5]) {
    static float old_out[] = {2.0, 2.0, 2.0, 2.0, 2.0};

    /* Set all thurster values */
    if(fabs(old_out[BOW] - out[BOW]) > UPDATE_TOLERANCE) {
        old_out[BOW] = out[BOW];
        Var_set("Bow", out[BOW]);
    }

    if(fabs(old_out[STERN] - out[STERN]) > UPDATE_TOLERANCE) {
        old_out[STERN] = out[STERN];
        Var_set("Stern", out[STERN]);
    }

    if(fabs(old_out[PORT] - out[PORT]) > UPDATE_TOLERANCE) {
        old_out[PORT] = out[PORT];
        Var_set("Port", out[PORT]);
    }

    if(fabs(old_out[STAR] - out[STAR]) > UPDATE_TOLERANCE) {
        old_out[STAR] = out[STAR];
        Var_set("Star", out[STAR]);
    }

    if(fabs(old_out[STRAFE] - out[STRAFE]) > UPDATE_TOLERANCE) {
        old_out[STRAFE] = out[STRAFE];
        Var_set("Strafe", out[STRAFE]);
    }
}

static int count;
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
    float out[] = {0.0, 0.0, 0.0, 0.0, 0.0};
    
    /* Value requests from PID's */
    float req_strafe  = 0.0;
    float req_pitch   = 0.0;
    float req_depth   = 0.0;
    float req_forward = 0.0;
    float req_yaw     = 0.0;

    /* Notify buffers */
    char data[64];
    char requester[16], value[16];

    /* Zero thrusters */
    setThrusters(out);

    /* Notify filters */
    Notify_filter(FILTER_ACTION, "THRUSTER_REQUEST");
    Notify_send("GO", "MissionControl");
    
    count = 0;
    Task_background(rate);

    while(true) {
        Notify_get(NULL, data);
        Util_split(data, ' ', requester, value);

        count++;

        /* Parse request */
        if(strcmp(requester, "Yaw") == 0) {
            req_yaw = atof(value);
        } else if(strcmp(requester, "Forward") == 0) {
            req_forward = atof(value);
        } else if(strcmp(requester, "Pitch") == 0) {
            req_pitch = atof(value);
        } else if(strcmp(requester, "Depth") == 0) {
            req_depth = atof(value);
        } else if(strcmp(requester, "Strafe") == 0) {
            req_strafe = atof(value);
        } else {
            continue;
        }

        /* Mix */
        mix(req_pitch, req_depth, req_forward, req_yaw, req_strafe, out);

        /* Check bounds on all output values */
        out[BOW]    = Util_inRange(-THRUSTER_MAX, out[BOW], THRUSTER_MAX);
        out[STERN]  = Util_inRange(-THRUSTER_MAX, out[STERN], THRUSTER_MAX);
        out[STRAFE] = Util_inRange(-THRUSTER_MAX, out[STRAFE], THRUSTER_MAX);
        out[PORT]   = Util_inRange(-THRUSTER_MAX, out[PORT], THRUSTER_MAX);
        out[STAR]   = Util_inRange(-THRUSTER_MAX, out[STAR], THRUSTER_MAX);

        /* Output new thruster values */
        setThrusters(out);
    }

    Seawolf_close();
    return 0;
}

