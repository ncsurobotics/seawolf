
#ifndef __SEAWOLF_STACK_INCLUDE_H
#define __SEAWOLF_STACK_INCLUDE_H

#define _STACK_BLOCK_SIZE 16

struct Stack_s {
    void** base;
    int index;
};

typedef struct Stack_s Stack;

Stack* Stack_new(void);
void Stack_push(Stack* stack, void* v);
void* Stack_pop(Stack* stack);
void* Stack_top(Stack* stack);
int Stack_getSize(Stack* stack);
void Stack_destroy(Stack* stack);

#endif // #ifndef __SEAWOLF_STACK_INCLUDE_H
