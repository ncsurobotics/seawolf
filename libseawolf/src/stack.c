/**
 * \file
 * \brief Stack
 */

#include "seawolf.h"

/**
 * Amount to grow stack by when more space is needed
 * \private
 */
#define STACK_BLOCK_SIZE 16

/**
 * \defgroup Stack Stack
 * \ingroup DataStructures
 * \brief Stack data structure implmentation
 * \sa http://en.wikipedia.org/wiki/Stack_%28data_structure%29
 * \{
 */

/**
 * \brief Create a new stack
 *
 * Create a new, empty LIFO stack
 *
 * \return A new stack
 */
Stack* Stack_new(void) {
    Stack* stack = malloc(sizeof(Stack));
    
    if(stack == NULL) {
        return NULL;
    }
    
    stack->base = (void**) malloc(sizeof(void*) * STACK_BLOCK_SIZE);
    if(stack->base == NULL) {
        free(stack);
        return NULL;
    }

    stack->index = 0;
    return stack;
}

/**
 * \brief Push onto the stack
 *
 * Push a new value onto the stack
 *
 * \param stack The stack to push to
 * \param v The value to push
 */
void Stack_push(Stack* stack, void* v) {
    /* Insert record */
    stack->base[stack->index++] = v;

    /* Possibly resize */
    if(stack->index % STACK_BLOCK_SIZE == 0) {
        stack->base = (void**) realloc(stack->base, sizeof(void*) * (stack->index + STACK_BLOCK_SIZE));
    }
}

/**
 * \brief Pop a value off the stack
 *
 * Pop the element off the top of the stack
 *
 * \param stack The stack to pop off of
 * \return The value popped off or NULL if the stack is empty
 */
void* Stack_pop(Stack* stack) {
    if(stack->index == 0) {
        return NULL;
    }

    /* Obtain record */
    void* v = stack->base[--stack->index];

    /* Possibly resize */
    if((stack->index + 1) % STACK_BLOCK_SIZE == 0) {
        stack->base = (void**) realloc(stack->base, sizeof(void*) * (stack->index + 1));
    }

    return v;
}

/**
 * \brief Get the top element of the stack
 *
 * Get the element off the top of the stack without removing it
 *
 * \param stack To get top element of
 * \return The value off the top of the stack
 */
void* Stack_top(Stack* stack) {
    return stack->base[stack->index - 1];
}

/**
 * \brief Get the size of the stack
 *
 * Retrieve the number of elements in the stack
 *
 * \param stack The stack to get the size of
 * \return The number of elements in the stack
 */
int Stack_getSize(Stack* stack) {
    return stack->index;
}

/**
 * \brief Destroy a stack
 *
 * Free a stack. This does not free any memory associated with elements of the stack. This must be freed separately
 *
 * \param stack The stack to free
 */
void Stack_destroy(Stack* stack) {
    free(stack->base);
    free(stack);
}

/** \} */
