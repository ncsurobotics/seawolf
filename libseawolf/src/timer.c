/**
 * \file
 * \brief Timer
 */

#include "seawolf.h"

#include <time.h>

/**
 * Compute the time difference in seconds between two timespec structures
 *
 * \private
 * \param t Base time
 * \param s New time
 * \return Timer difference in seconds
 */
#define _TIMESPEC_DIFF(/* struct timespec */ t, /* struct timespec */ s) \
    ((double)((s).tv_sec - (t).tv_sec) + (((double)(s).tv_nsec - (t).tv_nsec) / 1e9))

/**
 * \defgroup Timer Timer
 * \ingroup Utilities
 * \brief Timers for calculating total time and time delays
 * \{
 */

/**
 * \brief Return a new Timer object
 *
 * Return a new timer object
 *
 * \return A new timer
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
 * \brief Get a time delta
 *
 * Return the time delta in seconds since the last call to Timer_getDelta() or
 * since the Timer was created
 *
 * \param tm The timer to get the delta for
 * \return Seconds since the timer being created or the last call to
 * Timer_getDelta()
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
 * \brief Get total time delay
 *
 * Get the time delta in seconds since the Timer was created or last reset
 *
 * \param tm The timer to get the delay for
 * \return Seconds since timer reset or timer creation
 */
double Timer_getTotal(Timer* tm) {
    struct timespec now;
    double diff;
    
    clock_gettime(CLOCK_REALTIME, &now);
    diff = _TIMESPEC_DIFF(tm->base, now);

    return diff;
}

/**
 * \brief Reset the timer
 *
 * Reset the timer's base time
 *
 * \param tm The timer to reset
 */
void Timer_reset(Timer* tm) {
    /* Store the time into base and copy to last */
    clock_gettime(CLOCK_REALTIME, &tm->base);
    tm->last = tm->base;
}

/**
 * \brief Destroy the timer
 *
 * Free the memory associated with the timer
 * 
 * \param tm The timer to free
 */
void Timer_destroy(Timer* tm) {
    free(tm);
}

/** \} */
