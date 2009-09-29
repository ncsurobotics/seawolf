
#ifndef __SEAWOLF_TIMER_INCLUDE_H
#define __SEAWOLF_TIMER_INCLUDE_H

#define _POSIX_C_SOURCE 199309L
#include <time.h>

struct Timer_s {
    struct timespec base;
    struct timespec last;
};

typedef struct Timer_s Timer;

Timer* Timer_new(void);
double Timer_getDelta(Timer* tm);
double Timer_getTotal(Timer* tm);
void Timer_reset(Timer* tm);
void Timer_destroy(Timer* tm);

#endif // #ifndef __SEAWOLF_TIMER_INCLUDE_H
