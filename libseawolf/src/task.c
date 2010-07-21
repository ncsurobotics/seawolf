/**
 * \file
 * \brief Task scheduling and backgrounding
 */

#include "seawolf.h"

#include <stdarg.h>
#include <pthread.h>
#include <unistd.h>

/**
 * Maximum number of arguments to the Task_spawnApplication
 * \private
 */
#define MAX_ARGS 31

/**
 * Task completed successfully
 * \private
 */
#define TASK_SUCCESS 0

/**
 * Task is to be retried
 * \private
 */
#define TASK_RETRY   1

/**
 * Task failed to run successfully
 * \private
 */
#define TASK_GIVEUP  2

/**
 * Arguments passed to Task_callWrapper()
 */
struct WrapperArgs {
    /**
     * The function to be called
     */
    int (*func)(void);
    
    /**
     * Return value of func() stored here
     */
    int return_value;
    
    
    /**
     * Should Task_callWrapper free this structure
     */
    bool free;
};

/**
 * Arguments passed to Task_watcher()
 */
struct WatcherArgs {
    /**
     * Thread to watch
     */
    pthread_t* dependant;

    /**
     * How long to wait
     */
    double timeout;
};

static void* Task_callWrapper(void* _args);
static void* Task_watcher(void* _args);
static TaskQueueNode* TaskQueueNode_new(Task* task);
static void TaskQueueNode_destroy(TaskQueueNode* node);
static void TaskQueue_insertAfter(TaskQueue* tq, TaskQueueNode* base, TaskQueueNode* node);
static TaskQueueNode* TaskQueue_remove(TaskQueue* tq, TaskQueueNode* node);

/**
 * \defgroup Task Task scheduling and management
 * \ingroup Utilities
 * \brief Utilities for scheduling tasks and performing simple multitasking
 * \{
 */

/**
 * \brief Call wrapper for task calls
 *
 * Given a WrapperArgs, call WrapperArgs->func, store the return value in
 * WrapperArgs->return_value and possible free the WrapperArgs
 *
 * \param _args A WrapperArgs pointer cast to void*
 * \return NULL
 */
static void* Task_callWrapper(void* _args) {
    struct WrapperArgs* args = (struct WrapperArgs*) _args;
    args->return_value = args->func();

    if(args->free) {
        free(args);
    }
    return NULL;
}

/**
 * \brief Call wrapper for watchdog
 *
 * _args is cast to a WatcherArgs pointer (args). This function sleeps, and if
 * it is not canceled before returning from the sleep call, cancels the thread
 * given by args->dependant
 *
 * \param _args A WatcherArgs pointer cast to void*
 * \return NULL
 */
static void* Task_watcher(void* _args) {
    struct WatcherArgs* args = (struct WatcherArgs*)_args;
    Util_usleep(args->timeout);
    pthread_cancel(*args->dependant);
    return NULL;
}

/**
 * \brief Run a function with a timeout
 *
 * Watchdog on a function call. Returns WATCHDOG_TIMEOUT on timeout
 *
 * \param timeout Number of seconds before returning WATCHDOG_TIMEOUT if the
 * function does not return sooner
 * \param func Function to call under the watchdog.
 * \return Returns the return value of the function or WATCHDOG_TIMEOUT in the
 * case of timeout
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

/**
 * \brief Spawn a function in a new thread
 *
 * Run a new thread to run the given function in and return without waiting for
 * completion
 * 
 * \param func The function to spawn
 * \return A Task handle object
 */
Task_Handle Task_background(int (*func)(void)) {
    pthread_t func_th;
    struct WrapperArgs* func_args = malloc(sizeof(struct WrapperArgs));

    func_args->func = func;
    func_args->return_value = 0;
    func_args->free = true;

    pthread_create(&func_th, NULL, Task_callWrapper, func_args);
    return func_th;
}

/**
 * \brief Spawn an external program
 *
 * Spawn an external application and run asychronously with the current
 * application i.e. it returns almost immediately
 *
 * \param path Application to be run
 * \param args A NULL terminated list of program arguments
 * \return -1 on failure, otherwise the PID of spawned application is returned
 */
pid_t Task_spawnApplication(const char* path, char* args, ...) {
    int pid;
    va_list ap;
    char* argv[MAX_ARGS + 1];

    /* Build arguments array */
    argv[0] = path;
    argv[1] = NULL;

    va_start(ap, args);
    for(int i = 1; i < MAX_ARGS && args != NULL; i++) {
        argv[i] = args;
        argv[i+1] = NULL;
        args = va_arg(ap, char*);
    }
    va_end(ap);

    /* Run program */
    pid = fork();
    if(pid == 0) {
        /* Replace current process with the given application */
        execv(path, argv);
        
        /* Should *not* happen */
        fprintf(stderr, "Application %s failed to spawn!\n", path);
        exit(EXIT_FAILURE);
    }

    return pid;
}

/**
 * \brief Kill a running task
 *
 * Kill a task previously spawned by Task_background()
 *
 * \param task The Task handle associated with the task to kill
 */
void Task_kill(Task_Handle task) {
    pthread_cancel(task);
    pthread_join(task, NULL);
}

/**
 * \brief Wait for a task to terminate
 *
 * Wait for a task to terminate
 *
 * \param task The task handle associated with the task to wait for
 */
void Task_wait(Task_Handle task) {
    pthread_join(task, NULL);
}

/**
 * \brief Create a new task
 *
 * Create a new task associated with the given function that can be added to a
 * TaskQueue
 *
 * \param func A function to associated with task with. When the task is called,
 * this function will be called
 * \return A new Task object
 */
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

/**
 * \brief Destroy a Task object
 *
 * Free the memory allocated to the given Task object
 *
 * \param task The Task object to destroy
 */
void Task_destroy(Task* task) {
    free(task);
}

/**
 * \brief Run a Task
 *
 * Run the function associated with the given Task object
 *
 * \param task The task to run
 * \return Success status of the task
 */
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
 * \brief Create a new TaskQueue
 *
 * Create a new TaskQueue object
 *
 * \return A new TaskQueue
 */
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

/**
 * \brief Destroy a TaskQueue
 *
 * Destroy the given TaskQueue
 *
 * \param tq The TaskQueue to free
 */
void TaskQueue_destroy(TaskQueue* tq) {
    free(tq);
}

/**
 * \brief Create a new TaskQueueNode
 * 
 * Create a new TaskQueueNode
 *
 * \param task The task to store into the TaskQueueNode
 * \return A new TaskQueueNode
 */
static TaskQueueNode* TaskQueueNode_new(Task* task) {
    TaskQueueNode* node = malloc(sizeof(TaskQueueNode));
    if(node == NULL) {
        return NULL;
    }

    node->task = task;
    return node;
}

/**
 * \brief Destoy a TaskQueueNode
 * 
 * Destoy a TaskQueueNode
 *
 * \param node The TaskQueueNode to destroy
 */
static void TaskQueueNode_destroy(TaskQueueNode* node) {
    free(node);
}

/**
 * \brief Insert a TaskQueueNode
 *
 * Insert a TaskQueueNode into a TaskQueue
 *
 * \param tq The TaskQueue to insert into
 * \param base The TaskQueueNode to insert after
 * \param node The TaskQueueNode to insert
 */
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

/**
 * \brief Remove a TaskQueueNode
 *
 * Remove a TaskQueueNode from a TaskQueue
 *
 * \param tq TaskQueue to remove from
 * \param node The TaskQueueNode to remove
 * \return The node that was removed
 */
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

/**
 * \brief Append a task to a TaskQueue
 *
 * Append the given Task to the TaskQueue
 *
 * \param tq The TaskQueue to append to
 * \param task The Task to append
 */
void TaskQueue_addTask(TaskQueue* tq, Task* task) {
    /* Insert new task at the end of the queue */
    TaskQueue_insertAfter(tq, tq->last, TaskQueueNode_new(task));
}

/**
 * \brief Run a TaskQueue
 *
 * Run a TaskQueue. This involves running all Task sequentially and requeueing
 * failed tasks if TASK_RETRY is set until the TaskQueue is emptied.
 *
 * \param tq The TaskQueue to run
 */
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

/** \} */
