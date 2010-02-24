 
#ifndef __SEAWOLF_QUEUE_INCLUDE_H
#define __SEAWOLF_QUEUE_INCLUDE_H

#include "seawolf.h"

struct Queue_s {
    List* list;
    pthread_mutex_t lock;
    pthread_cond_t available;
};

typedef struct Queue_s Queue;

Queue* Queue_new(void);
void Queue_append(Queue* queue, void* v);
void* Queue_pop(Queue* queue, bool wait);
int Queue_getSize(Queue* queue); 
void Queue_destroy(Queue* queue);

#endif // #ifndef __SEAWOLF_QUEUE_INCLUDE_H

