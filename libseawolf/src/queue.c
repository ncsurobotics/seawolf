
#include "seawolf.h"

#include <pthread.h>

Queue* Queue_new(void) {
    Queue* queue = malloc(sizeof(Queue));
    queue->list = List_new();

    pthread_mutex_init(&(queue->lock), NULL);
    pthread_cond_init(&(queue->available), NULL);
    return queue;
}

void Queue_append(Queue* queue, void* v) {
    pthread_mutex_lock(&(queue->lock));
    List_append(queue->list, v);
    pthread_cond_signal(&(queue->available));
    pthread_mutex_unlock(&(queue->lock));
}

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

int Queue_getSize(Queue* queue) {
    return List_getSize(queue->list);
}

void Queue_destroy(Queue* queue) {
    List_destroy(queue->list);
    free(queue);
}
