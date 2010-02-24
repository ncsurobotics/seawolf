
/*
 * Multi dimensional PID to do tracking of spherical points relative to the ship
 */

#include "seawolf.h"

#include "math.h"

/* Indexes */
#define THETA 0
#define PHI 1
#define RHO 2

/* Attempt to correct the leftward drift */
#define THETA_SKEW 2.2

/* PID Parameters */
#define THETA_Kp 1
#define THETA_Ki 0
#define THETA_Kd 0
#define PHI_Kp 1
#define PHI_Ki 0
#define PHI_Kd 0
#define RHO_Kp 2
#define RHO_Ki 0
#define RHO_Kd 0

static void dataOut(double mv[3], bool do_depth, bool do_yaw) {
    /* Base value for horizontal thrusters */
    float port_x, star_x;
    port_x = Util_inRange(-THRUSTER_MAX, mv[RHO], THRUSTER_MAX);
    star_x = Util_inRange(-THRUSTER_MAX, mv[RHO], THRUSTER_MAX);
    
    /* Offset for yaw */
    if(do_yaw) {
        port_x += mv[THETA];
        star_x -= mv[THETA];

        /* Bounds check again */
        port_x = Util_inRange(-THRUSTER_MAX, port_x, THRUSTER_MAX);
        star_x = Util_inRange(-THRUSTER_MAX, star_x, THRUSTER_MAX);
    }

    /* Send out to thrusters */    
    Notify_send("THRUSTER_REQUEST", Util_format("Forward %d %d", (int) port_x, (int) star_x));

    if(do_depth) {
        Var_set("DepthHeading", Var_get("Depth") + mv[PHI]);
    }
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Object Tracking");

    /* Timer for each PID */
    Timer* timer = Timer_new();

    /* Temporary variables */
    double e[3] = {0, 0, 0};
    double delta_t;
    double adjusted_rho_Kp;

    /* Previous error */
    double e_last[3];

    /* Running error */
    double e_dt[3] = {0.0, 0.0, 0.0};

    /* Set point is always the zero vector */
    const float sp[3] = {0, 0, 0};
    double pv[3], mv[3];

    /* Tracker controls depth */
    bool do_depth = (Var_get("TrackerDoDepth") == 1.0);
    bool do_yaw = true;

    /* Notify buffers */
    char action[16], data[16];

    /* Only receive SetPoint updates */
    Notify_filter(FILTER_MATCH, "UPDATED SetPoint");
    Notify_filter(FILTER_MATCH, "UPDATED TrackerDoDepth");

    Timer_reset(timer);
    while(true) {
        Notify_get(action, data);
        if(strcmp(data, "TrackerDoDepth") == 0) {
            do_depth = (Var_get("TrackerDoDepth") == 1.0);
            continue;
        }

        /* Store delta_t */
        delta_t = Timer_getDelta(timer);

        /* Get process variable */
        pv[THETA] = Var_get("SetPoint.Theta");
        pv[PHI] = Var_get("SetPoint.Phi");
        pv[RHO] = Var_get("SetPoint.Rho");

        if(pv[THETA] == 0 && do_yaw) {
            Var_set("PIDDoYaw", 1.0);
            do_yaw = 0.0;
            Var_set("YawHeading", Var_get("SEA.Yaw"));
            Logging_log(DEBUG, "Switch to straight path");
        } else if(pv[THETA] != 0 && !do_yaw) {
            Var_set("PIDDoYaw", 0.0);
            do_yaw = 1.0;
            Logging_log(DEBUG, "Switch to tracking path");
        }
        
        /* Copy old error */
        e_last[THETA] = e[THETA];
        e_last[PHI] = e[PHI];
        e_last[RHO] = e[RHO];

        /* Compute errors */
        e[THETA] = pv[THETA] - sp[THETA];
        e[PHI] = pv[PHI] - sp[PHI];
        e[RHO] = pv[RHO] - sp[RHO];

        /* Add integrate error */
        e_dt[THETA] += delta_t * e[THETA];
        e_dt[PHI] += delta_t * e[PHI];
        e_dt[RHO] += delta_t * e[RHO];

        /* Compute manipulated variable */
        mv[THETA] = (THETA_Kp * e[THETA]) +    \
                    (THETA_Ki * e_dt[THETA]) + \
                    (THETA_Kd * ((e[THETA] - e_last[THETA]) / delta_t));

        mv[PHI] = (PHI_Kp * e[PHI]) +    \
                  (PHI_Ki * e_dt[PHI]) + \
                  (PHI_Kd * ((e[PHI] - e_last[PHI]) / delta_t));

        /* Let the proprotional coefficient for phi be inversely proprotional to the error in theta and phi */
        adjusted_rho_Kp = RHO_Kp * (1 - (sqrt(pow(e[THETA], 2) + pow(e[PHI], 2))/(180 * M_SQRT2)));
        mv[RHO] = (adjusted_rho_Kp * e[RHO]) +   \
                  (RHO_Ki * e_dt[RHO]) + \
                  (RHO_Kd * ((e[RHO] - e_last[RHO]) / delta_t));
        
        /* Send data out */
        dataOut(mv, do_depth, do_yaw);
    }

    Timer_destroy(timer);
    Seawolf_close();
    return 0;
}
