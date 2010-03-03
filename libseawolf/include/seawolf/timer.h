/**
 * \file
 */

#ifndef __SEAWOLF_TIMER_INCLUDE_H
#define __SEAWOLF_TIMER_INCLUDE_H

/** \private */
#define _POSIX_C_SOURCE 199309L
#include <time.h>

/**
 * Timer
 */
typedef struct {
    /**
     * Starting time
     * \private
     */
    struct timespec base;

    /**
     * Time at last delta
     * \private
     */
    struct timespec last;
} Timer;

Timer* Timer_new(void);
double Timer_getDelta(Timer* tm);
double Timer_getTotal(Timer* tm);
void Timer_reset(Timer* tm);
void Timer_destroy(Timer* tm);

#endif // #ifndef __SEAWOLF_TIMER_INCLUDE_H
