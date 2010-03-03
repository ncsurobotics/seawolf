/**
 * \file
 * \brief PID controller
 */

#include "seawolf.h"

/**
 * \defgroup PID Proportional-Integral-Derivative (PID) controller
 * \ingroup Utilities
 * \brief Provides an implementation of a Proportional-Integral-Derivative (PID) controller
 * \sa http://en.wikipedia.org/wiki/PID_Controller
 * \{
 */

/**
 * \brief Create a new PID controller object
 *
 * Instantiates a new PID controller object associated with the given set point
 * and coefficients
 *
 * \param sp The initial set point for the PID
 * \param p Initial proportional coefficient
 * \param i Initial integral coefficient
 * \param d Initial differential coefficient
 * \return The new PID object
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
 * \brief Start/reset the PID
 *
 * Starts/resets the PID. This should be called if the set point is
 * altered. This function returns an initial manipulated variable, though since
 * no differential component can be calculated yet, and the integral component
 * will be zero, this returned value is based only on the proportional part of
 * the controller p*(pv-mv)
 *
 * \param pid The controller object
 * \param pv The value of an initial process variable
 * \return A "best guess" initial manipulated variable (mv) as described above
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
 * \brief Update and return the manipulated variable based on the new process variable
 *
 * Return the new value of the maniuplated variable (mv) based on the new value
 * of the given process variable (pv)
 * 
 * \param pid The controller object
 * \param pv The new process variable (pv)
 * \return The new manipulated variable after considering the new process variable
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
 * \brief Reset the integral component
 *
 * Reset the cumulative error associated with the integral component of the
 * controller to 0
 *
 * \param pid The controller object
 */
void PID_resetIntegral(PID* pid) {
    pid->e_dt = 0;
}

/**
 * \brief Change the set point for the controller
 *
 * Change the set point (sp) for the controller. It is a good idea to reset the
 * controller after calling this
 *
 * \param pid The controller object
 * \param sp The new set point for the controller
 */
void PID_setSetPoint(PID* pid, double sp) {
    pid->sp = sp;
}

/**
 * \brief Change coefficients
 *
 * Change the coefficients associated with the controller
 *
 * \param pid The controller object
 * \param p The proportional coefficient
 * \param i The integral coefficient
 * \param d The differential coefficient
 */
void PID_setCoefficients(PID* pid, double p, double i, double d) {
    pid->p = p;
    pid->i = i;
    pid->d = d;
}

/**
 * \brief Destroy the controller object
 *
 * Destroy and free the memory associated with the given controller
 *
 * \param pid The controller object
 */
void PID_destroy(PID* pid) {
    Timer_destroy(pid->timer);
    free(pid);
}

/** \} */
