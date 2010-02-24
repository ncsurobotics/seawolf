
#include "seawolf.h"

#include <pthread.h>
#include <stdbool.h>

#define TASK_SUCCESS 0
#define TASK_RETRY   1
#define TASK_GIVEUP  2

/*
 * Function call watchdog 
 */ 

struct WrapperArgs {
    int (*func)(void);
    int return_value;
    bool free; /* Free this structure at the end of Task_callWrapper */
};

struct WatcherArgs {
    pthread_t* dependant;
    double timeout;
};

static void* Task_callWrapper(void* _args) {
    struct WrapperArgs* args = (struct WrapperArgs*) _args;
    args->return_value = args->func();

    if(args->free) {
        free(args);
    }
    return NULL;
}

static void* Task_watcher(void* _args) {
    struct WatcherArgs* args = (struct WatcherArgs*)_args;
    Util_usleep(args->timeout);
    pthread_cancel(*args->dependant);
    return NULL;
}

/**
 * Watchdog on a function call. Returns WATCHDOG_TIMEOUT on timeout
 */
int Task_watchdog(double timeout, int (*func)(void)) {
    pthread_t func_th;
    pthread_t watchdog_th;
    struct WrapperArgs func_args = {func, WATCHDOG_TIMEOUT, false};
    struct WatcherArgs watchdog_args = {&func_th, timeout};

    pthread_create(&func_th, NULL, Task_callWrapper, &func_args);
    pthread_create(&watchdog_th, NULL, Task_watcher, &watchdog_args);

    /* Wait for main function - may be canceled by watcher */
    pthread_join(func_th, NULL);
    
    /* Cancel and wait for watcher */
    pthread_cancel(watchdog_th);
    pthread_join(watchdog_th, NULL);

    return func_args.return_value;
}

Task_Handle Task_background(int (*func)(void)) {
    pthread_t func_th;
    struct WrapperArgs* func_args = malloc(sizeof(struct WrapperArgs));

    func_args->func = func;
    func_args->return_value = 0;
    func_args->free = true;

    pthread_create(&func_th, NULL, Task_callWrapper, func_args);
    return func_th;
}

void Task_kill(Task_Handle task) {
    pthread_cancel(task);
    pthread_join(task, NULL);
}

void Task_wait(Task_Handle task) {
    pthread_join(task, NULL);
}

Task* Task_new(int (*func)(void)) {
    Task* task = malloc(sizeof(Task));
    if(task == NULL) {
        return NULL;
    }

    task->func = func;
    task->timeout = NO_TIMEOUT;
    task->retry = false;
    task->runs = 0;
    task->running = false;
    task->return_value = 0;
    
    return task;
}

void Task_destroy(Task* task) {
    free(task);
}

int Task_run(Task* task) {
    task->running = true;
    task->runs++;

    if(task->timeout == NO_TIMEOUT) {
        /* No timeout */
        task->return_value = task->func();
    } else {
        /* Timeout */
        task->return_value = Task_watchdog(task->timeout, task->func);
    }

    task->running = false;
    if(task->return_value == 0) {
        return TASK_SUCCESS;
    } else if(task->retry) {
        return TASK_RETRY;
    } else {
        return TASK_GIVEUP;
    }
}


/**
 * Task queue methods
 **/ 

TaskQueue* TaskQueue_new(void) {
    TaskQueue* tq = malloc(sizeof(TaskQueue));
    if(tq == NULL) {
        return NULL;
    }

    tq->first = NULL;
    tq->last = NULL;
    tq->count = 0;

    return tq;
}

void TaskQueue_destroy(TaskQueue* tq) {
    free(tq);
}

static TaskQueueNode* TaskQueueNode_new(Task* task) {
    TaskQueueNode* node = malloc(sizeof(TaskQueueNode));
    if(node == NULL) {
        return NULL;
    }

    node->task = task;
    return node;
}

static void TaskQueueNode_destroy(TaskQueueNode* node) {
    free(node);
}

static void TaskQueue_insertAfter(TaskQueue* tq, TaskQueueNode* base, TaskQueueNode* node) {
    if(tq->count == 0) {
        /* Insert into empty */
        tq->first = tq->last = node;
    } else if(base == NULL) {
        /* Insert at head */
        node->prev = NULL;
        node->next = tq->first;
        tq->first->prev = node;
        tq->first = node;
    } else if(base == tq->last) {
        /* Insert at tail */
        node->prev = tq->last;
        node->next = NULL;
        tq->last->next = node;
        tq->last = node;
    } else {
        /* Insert elsewhere (in the middle of a non-empty list) */
        node->prev = base;
        node->next = base->next;
        base->next = base;
        node->next->prev = node;
    }

    tq->count++;
}

static TaskQueueNode* TaskQueue_remove(TaskQueue* tq, TaskQueueNode* node) {
    if(tq->count == 1) {
        /* Remove last element */
        tq->first = tq->last = NULL;
    } else if(node == tq->first) {
        /* Remove first element */
        tq->first = node->next;
        tq->first->prev = NULL;
    } else if(node == tq->last) {
        /* Remove last element */
        tq->last = node->prev;
        tq->last->next = NULL;
    } else {
        /* Remove middle element */
        node->prev->next = node->next;
        node->next->prev = node->prev;
    }

    tq->count--;
    return node;
}

void TaskQueue_addTask(TaskQueue* tq, Task* task) {
    /* Insert new task at the end of the queue */
    TaskQueue_insertAfter(tq, tq->last, TaskQueueNode_new(task));
}

void TaskQueue_run(TaskQueue* tq) {
    TaskQueueNode* node;
    int return_value;
    while(tq->count > 0) {
        node = TaskQueue_remove(tq, tq->first);
        return_value = Task_run(node->task);

        if(return_value == TASK_RETRY) {
            TaskQueue_insertAfter(tq, tq->last, node);
        } else {
            /* Success or give up - either way destroy the node */
            TaskQueueNode_destroy(node);
        }
    }
}
