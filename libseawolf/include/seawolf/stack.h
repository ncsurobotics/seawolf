/**
 * \file
 */

#ifndef __SEAWOLF_STACK_INCLUDE_H
#define __SEAWOLF_STACK_INCLUDE_H

/**
 * Stack
 */
typedef struct {
    /**
     * Base data address
     * \private
     */
    void** base;

    /**
     * Top of stack
     * \private
     */
    int index;
} Stack;

Stack* Stack_new(void);
void Stack_push(Stack* stack, void* v);
void* Stack_pop(Stack* stack);
void* Stack_top(Stack* stack);
int Stack_getSize(Stack* stack);
void Stack_destroy(Stack* stack);

#endif // #ifndef __SEAWOLF_STACK_INCLUDE_H
