
#ifndef __SEAWOLF_PID_INCLUDE_H
#define __SEAWOLF_PID_INCLUDE_H

#include "seawolf.h"

struct PID_s {
    Timer* timer;

    double p;
    double i;
    double d;

    double sp;

    double e_last;
    double e_dt;
};

typedef struct PID_s PID;

PID* PID_new(double sp, double p, double i, double d);
double PID_start(PID* pid, double pv);
double PID_update(PID* pid, double pv);
void PID_resetIntegral(PID* pid);
void PID_setCoefficients(PID* pid, double p, double i, double d);
void PID_setSetPoint(PID* pid, double sp);
void PID_destroy(PID* pid);

#endif // #ifndef __SEAWOLF_PID_INCLUDE_H
