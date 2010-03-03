/**
 * \file
 */
 
#ifndef __SEAWOLF_QUEUE_INCLUDE_H
#define __SEAWOLF_QUEUE_INCLUDE_H

#include "seawolf.h"

/**
 * Queue
 */
typedef struct {
    /**
     * List which backs the Queue
     * \private
     */
    List* list;

    /**
     * Queue mutex lock
     * \private
     */
    pthread_mutex_t lock;

    /**
     * Queue new item conditional
     * \private
     */
    pthread_cond_t available;
} Queue;

Queue* Queue_new(void);
void Queue_append(Queue* queue, void* v);
void* Queue_pop(Queue* queue, bool wait);
int Queue_getSize(Queue* queue); 
void Queue_destroy(Queue* queue);

#endif // #ifndef __SEAWOLF_QUEUE_INCLUDE_H

