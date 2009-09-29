
#include "seawolf.h"

#include <stdlib.h>
#include <time.h>

#define _TIMESPEC_DIFF(/* struct timespec */ t, /* struct timespec */ s) \
    ((double)((s).tv_sec - (t).tv_sec) + (((double)(s).tv_nsec - (t).tv_nsec) / 1e9))

/**
 * Return a new Timer object
 */
Timer* Timer_new(void) {
    Timer* tm = malloc(sizeof(Timer));
    if(tm == NULL) {
        return NULL;
    }

    /* Rest the timer */
    Timer_reset(tm);

    return tm;
}

/**
 * Return the time delta in seconds since the last call to Timer_getDelta or
 * since the Timer was created
 */
double Timer_getDelta(Timer* tm) {
    struct timespec now;
    double diff;
    
    clock_gettime(CLOCK_REALTIME, &now);
    diff = _TIMESPEC_DIFF(tm->last, now);
    tm->last = now;

    return diff;
}

/**
 * Get the time delta in seconds since the Timer was created or last reset
 */
double Timer_getTotal(Timer* tm) {
    struct timespec now;
    double diff;
    
    clock_gettime(CLOCK_REALTIME, &now);
    diff = _TIMESPEC_DIFF(tm->base, now);

    return diff;
}

/**
 * Reset the timer's base time
 */
void Timer_reset(Timer* tm) {
    /* Store the time into base and copy to last */
    clock_gettime(CLOCK_REALTIME, &tm->base);
    tm->last = tm->base;
}

/**
 * Deallocate the timer
 */
void Timer_destroy(Timer* tm) {
    free(tm);
}

