
#include "seawolf.h"

/**
 * Create a new PID object with the given set point and coefficients 
 */
PID* PID_new(double sp, double p, double i, double d) {
    PID* pid = malloc(sizeof(PID));
    if(pid == NULL) {
        return NULL;
    }

    pid->timer = Timer_new();

    pid->p = p;
    pid->i = i;
    pid->d = d;

    pid->sp = sp;

    pid->e_last = 0;
    pid->e_dt = 0;

    return pid;
}

/**
 * Starts/resets the PID. This should be called if the set point is altered
 */
double PID_start(PID* pid, double pv) {
    double e = pid->sp - pv;
    double mv;

    /* Zero running error, and store current error as last */
    pid->e_dt = 0;
    pid->e_last = e;
    Timer_reset(pid->timer);

    /* Initial run -- the safest thing to do is return only proportional term */
    mv = pid->p * e;
    return mv;
}

/**
 * Insert a new value and get a new output value
 */
double PID_update(PID* pid, double pv) {
    double delta_t = Timer_getDelta(pid->timer);
    double e = pid->sp - pv;
    double mv;
    
    /* Update running error */
    pid->e_dt += delta_t * e;

    /* Calculate output value */
    mv  = pid->p * e;
    mv += pid->i * pid->e_dt;
    mv += pid->d * ((e - pid->e_last) / delta_t);
    
    /* Store error */
    pid->e_last = e;

    return mv;
}

/**
 * Reset the running error to 0
 */
void PID_resetIntegral(PID* pid) {
    pid->e_dt = 0;
}

/**
 * Update the set point. The PID should be reset after this in most cases
 */
void PID_setSetPoint(PID* pid, double sp) {
    pid->sp = sp;
}

/**
 * Update coefficients
 */
void PID_setCoefficients(PID* pid, double p, double i, double d) {
    pid->p = p;
    pid->i = i;
    pid->d = d;
}

/**
 * Destroy and free the PID
 */
void PID_destroy(PID* pid) {
    Timer_destroy(pid->timer);
    free(pid);
}
