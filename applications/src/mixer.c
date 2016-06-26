
#include "seawolf.h"

#include <ncurses.h>
#include <pthread.h>
#include <math.h>

#define PORT    0
#define STAR    1
#define BOW     2
#define STERN   3
#define STRAFET 4
#define STRAFEB 5

/* Trim port/star values to compensate for rotation from strafing */
#define STRAFE_TRIM 0.3

/* Trim bow/stern values to compensate for pitch from diving/surfacing.
   Higher values make bow go faster.
 */
#define PITCH_TRIM 0.1

#define FORWARD_TRIM -0.4

#define UPDATE_TOLERANCE 0.01

/* Normalized linear trimming algorithm */
static void trim(float* outa, float* outb, float process_variable, float trim_value) {
    // check if anything bad is going to happen
    if ((trim_value > 1.0) || (trim_value < -1.0)) {
        printf("invalid trim value of %0.1f! Ignoring trim.\n", trim_value);
        return;
    }

    // update components
    if (trim_value > 0) {
        *outb -= process_variable * trim_value;
    }

    else if (trim_value < 0) {
        trim_value = -trim_value;
        *outa -= process_variable * trim_value;
    }

    return;
}

/* Simple summing mixing algorithm */
static void mix(float req_pitch, float req_depth, float req_forward, float req_yaw, float req_strafe, float req_roll, float out[6]) {
    /* 
    direction and       vectorized commands that typically come from
    magnitude of        sw3.routines.py. See high-level navigation
    thruster at         section of manual in order to understand which
    location [x].       direction each vector is pointing.
    -------------       --------------------------------------------- */
    out[BOW] = -req_pitch + req_depth;
    out[STERN] = req_pitch + req_depth;
    out[PORT] = req_forward + req_yaw;
    out[STAR] = req_forward - req_yaw;
    out[STRAFET] = req_strafe + req_roll;
    out[STRAFEB] = -req_strafe + req_roll;

    /* Trim port/starboad thrusters */
    //if(req_forward != 0) {
    //    out[PORT] += req_forward * FORWARD_TRIM;
    //    out[STAR] -= req_forward * FORWARD_TRIM;
    //}
    trim(&out[PORT], &out[STAR], req_forward, FORWARD_TRIM);

    /* Trim port/starboad thrusters */
    //if(req_strafe != 0) {
    //    out[STRAFET] += req_strafe * STRAFE_TRIM;
    //    out[STRAFEB] -= req_strafe * STRAFE_TRIM;
    //}
    trim(&out[STRAFET], &out[STRAFEB], req_strafe, STRAFE_TRIM);

    /* Trim bow/stern thrusters */
    //if(req_depth != 0) {
    //    out[STERN] -= req_depth * PITCH_TRIM;
    //    out[BOW] += req_depth * PITCH_TRIM;
    //}
    trim(&out[STERN], &out[BOW], req_depth, PITCH_TRIM);
}

static void setThrusters(float out[6]) {
    static float old_out[] = {2.0, 2.0, 2.0, 2.0, 2.0, 2.0};

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

    if(fabs(old_out[STRAFET] - out[STRAFET]) > UPDATE_TOLERANCE) {
        old_out[STRAFET] = out[STRAFET];
        Var_set("StrafeT", out[STRAFET]);
    }

    if(fabs(old_out[STRAFEB] - out[STRAFEB]) > UPDATE_TOLERANCE) {
        old_out[STRAFEB] = out[STRAFEB];
        Var_set("StrafeB", out[STRAFEB]);
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

static char data[64];
int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("PID Mixer");

    /* Thruster values */
    float out[] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

    /* Value requests from PID's */
    float req_strafe  = 0.0;
    float req_roll    = 0.0;
    float req_pitch   = 0.0;
    float req_depth   = 0.0;
    float req_forward = 0.0;
    float req_yaw     = 0.0;

    /* Notify buffers */
    char requester[16], value[16];

    /* Zero thrusters */
    setThrusters(out);

    /* Notify filters */
    Notify_filter(FILTER_ACTION, "THRUSTER_REQUEST");

    count = 0;
    Task_background(rate);

    while(true) {
        Notify_get(NULL, data);
        Util_split(data, ' ', requester, value);

        count++;

        /* Parse request */
        if (strcmp(requester, "Yaw") == 0) {
            req_yaw = atof(value);
        } else if(strcmp(requester, "Forward") == 0) {
            req_forward = atof(value);
        } else if(strcmp(requester, "Pitch") == 0) {
            req_pitch = atof(value);
        } else if(strcmp(requester, "Depth") == 0) {
            //printf("depth = %f\n", atof(value));
            req_depth = atof(value);
        } else if(strcmp(requester, "Strafe") == 0) {
            req_strafe = atof(value);
        } else if(strcmp(requester, "Roll") == 0) {
            req_roll = atof(value);
        } else {
            continue;
        }

        /* Mix */
        mix(req_pitch, req_depth, req_forward, req_yaw, req_strafe, req_roll, out);

        /* Check bounds on all output values */
        out[BOW]    = Util_inRange(-1, out[BOW], 1);
        out[STERN]  = Util_inRange(-1, out[STERN], 1);
        out[PORT]   = Util_inRange(-1, out[PORT], 1);
        out[STAR]   = Util_inRange(-1, out[STAR], 1);
        out[STRAFET] = Util_inRange(-1, out[STRAFET], 1);
        out[STRAFEB] = Util_inRange(-1, out[STRAFEB], 1);

        /* Output new thruster values */
        setThrusters(out);
    }

    Seawolf_close();
    return 0;
}

