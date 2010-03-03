/**
 * \file
 * \brief Queue
 */

#include "seawolf.h"

#include <pthread.h>

/**
 * \defgroup Queue Queue
 * \ingroup DataStructures
 * \brief A thread safe queue implemenation
 * \sa http://en.wikipedia.org/wiki/Queue_%28data_structure%29
 * \{
 */

/**
 * \brief Create a new queue
 *
 * Create a new, empty queue object. This is a FIFO queue.
 *
 * \return A new queue object
 */
Queue* Queue_new(void) {
    Queue* queue = malloc(sizeof(Queue));
    queue->list = List_new();

    pthread_mutex_init(&(queue->lock), NULL);
    pthread_cond_init(&(queue->available), NULL);
    return queue;
}

/**
 * \brief Append an item
 *
 * Append an item to the end of the queue
 *
 * \param queue The queue to append to
 * \param v The item to append
 */
void Queue_append(Queue* queue, void* v) {
    pthread_mutex_lock(&(queue->lock));
    List_append(queue->list, v);
    pthread_cond_signal(&(queue->available));
    pthread_mutex_unlock(&(queue->lock));
}

/**
 * \brief Pop an item off of the queue
 *
 * Get the next item off the top of the queue, if no items are available than
 * Queue_pop() can either block or return immediately
 *
 * \param queue The queue to pop from
 * \param wait If true, and no items are immediately available, then block until
 * an item becomes available and return it. Otherwise, return NULL immediately
 * if no items are available
 * \return The item popped or NULL if no items are available and wait is false
 */
void* Queue_pop(Queue* queue, bool wait) {
    void* v;

    pthread_mutex_lock(&queue->lock);
    while(wait && Queue_getSize(queue) == 0) {
        pthread_cond_wait(&queue->available, &queue->lock);
    }
    v = List_remove(queue->list, 0);
    pthread_mutex_unlock(&queue->lock);

    return v;
}

/**
 * \brief Get the size of the queue
 *
 * Return the number of elements in the queue
 *
 * \param queue The queue to return the size of
 * \return The number of items in the queue
 */
int Queue_getSize(Queue* queue) {
    return List_getSize(queue->list);
}

/**
 * \brief Destroy a Queue object
 *
 * Free the memory associated with the queue. Any memory allocated to items, in
 * the queue is not freed and should be done so separately
 * 
 * \param queue The queue to free
 */
void Queue_destroy(Queue* queue) {
    List_destroy(queue->list);
    free(queue);
}

/** \} */
