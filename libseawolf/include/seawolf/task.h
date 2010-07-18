/**
 * \file
 */

#ifndef __SEAWOLF_TASK_INCLUDE_H
#define __SEAWOLF_TASK_INCLUDE_H

#include <unistd.h>
#include <stdbool.h>
#include <pthread.h>

/**
 * Allow the function to run to completion (no watchdog)
 */
#define NO_TIMEOUT (-1.0)

/**
 * Returned in the case of a watchdog timeout
 */
#define WATCHDOG_TIMEOUT 255

/**
 * Task
 */
typedef struct {
    /**
     * Function to call
     * \private
     */
    int (*func)(void);

    /**
     * Function watchdog timeout
     */
    double timeout;

    /**
     * Retry function in case of failure
     */
    bool retry;

    /**
     * Number of times run
     * \private
     */
    int runs;

    /**
     * Currently running
     * \private
     */
    bool running;

    /**
     * Return value of the function called
     */
    int return_value;
} Task;

/**
 * TaskQueueNode
 * \private
 */
typedef struct TaskQueueNode_s {
    /**
     * Task for this node
     * \private
     */
    Task* task;

    /**
     * Next node
     * \private
     */
    struct TaskQueueNode_s* next;

    /**
     * Previous node
     * \private
     */
    struct TaskQueueNode_s* prev;
} TaskQueueNode;

/**
 * TaskQueue
 */
typedef struct {
    /**
     * Head
     * \private
     */
    TaskQueueNode* first;

    /**
     * Tail
     * \private
     */
    TaskQueueNode* last;
    
    /**
     * Task count
     * \private
     */
    int count;
} TaskQueue;

/**
 * Task handle used to refer to background tasks
 */
typedef pthread_t Task_Handle;

Task* Task_new(int (*func)(void));
void Task_destroy(Task* task);
int Task_run(Task* task);
int Task_watchdog(double timeout, int (*func)(void));
Task_Handle Task_background(int (*func)(void));
pid_t Task_spawnApplication(const char* path, char* args, ...);
void Task_kill(Task_Handle task);
void Task_wait(Task_Handle task);

TaskQueue* TaskQueue_new(void);
void TaskQueue_destroy(TaskQueue* tq);
void TaskQueue_addTask(TaskQueue* tq, Task* task);
void TaskQueue_run(TaskQueue* tq);

#endif // #ifndef __SEAWOLF_TASK_INCLUDE_H
