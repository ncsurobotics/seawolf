
#ifndef __SEAWOLF_TASK_INCLUDE_H
#define __SEAWOLF_TASK_INCLUDE_H

#include <stdbool.h>

#define NO_TIMEOUT (-1.0)
#define WATCHDOG_TIMEOUT 255

struct Task_s {
    int (*func)(void);
    double timeout;
    bool retry;
    int runs;
    bool running;
    int return_value;
};

struct TaskQueueNode_s {
    struct Task_s* task;
    struct TaskQueueNode_s* next;
    struct TaskQueueNode_s* prev;
};

struct TaskQueue_s {
    struct TaskQueueNode_s* first;
    struct TaskQueueNode_s* last;
    int count;
};

typedef struct Task_s Task;
typedef struct TaskQueue_s TaskQueue;
typedef struct TaskQueueNode_s TaskQueueNode;

Task* Task_new(int (*func)(void));
void Task_destroy(Task* task);
int Task_run(Task* task);
int Task_watchdog(double timeout, int (*func)(void));
void Task_background(int (*func)(void));

TaskQueue* TaskQueue_new(void);
void TaskQueue_destroy(TaskQueue* tq);
void TaskQueue_addTask(TaskQueue* tq, Task* task);
void TaskQueue_run(TaskQueue* tq);

#endif // #ifndef __SEAWOLF_TASK_INCLUDE_H
