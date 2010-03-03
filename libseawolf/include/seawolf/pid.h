/**
 * \file
 */

#ifndef __SEAWOLF_PID_INCLUDE_H
#define __SEAWOLF_PID_INCLUDE_H

#include "seawolf.h"

/**
 * PID
 */
typedef struct {
    /**
     * Timer used to determine time deltas
     * \private
     */
    Timer* timer;

    /**
     * Proportional coefficient
     * \private
     */
    double p;

    /**
     * Integral coefficient
     * \private
     */
    double i;

    /**
     * Derivative coefficient
     * \private
     */
    double d;

    /**
     * Set point
     * \private
     */
    double sp;

    /**
     * Last error
     * \private
     */
    double e_last;

    /**
     * Error integral
     * \private
     */
    double e_dt;
} PID;

PID* PID_new(double sp, double p, double i, double d);
double PID_start(PID* pid, double pv);
double PID_update(PID* pid, double pv);
void PID_resetIntegral(PID* pid);
void PID_setCoefficients(PID* pid, double p, double i, double d);
void PID_setSetPoint(PID* pid, double sp);
void PID_destroy(PID* pid);

#endif // #ifndef __SEAWOLF_PID_INCLUDE_H
