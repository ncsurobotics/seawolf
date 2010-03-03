
#include "seawolf.h"

#include <stdlib.h>

Stack* Stack_new(void) {
    Stack* stack = malloc(sizeof(Stack));
    
    if(stack == NULL) {
        return NULL;
    }
    
    stack->base = (void**) malloc(sizeof(void*) * _STACK_BLOCK_SIZE);
    if(stack->base == NULL) {
        free(stack);
        return NULL;
    }

    stack->index = 0;
    return stack;
}

void Stack_push(Stack* stack, void* v) {
    /* Insert record */
    stack->base[stack->index++] = v;

    /* Possibly resize */
    if(stack->index % _STACK_BLOCK_SIZE == 0) {
        stack->base = (void**) realloc(stack->base, sizeof(void*) * (stack->index + _STACK_BLOCK_SIZE));
    }
}

void* Stack_pop(Stack* stack) {
    if(stack->index == 0) {
        return NULL;
    }

    /* Obtain record */
    void* v = stack->base[--stack->index];

    /* Possibly resize */
    if((stack->index + 1) % _STACK_BLOCK_SIZE == 0) {
        stack->base = (void**) realloc(stack->base, sizeof(void*) * (stack->index + 1));
    }

    return v;
}

void* Stack_top(Stack* stack) {
    return stack->base[stack->index - 1];
}

int Stack_getSize(Stack* stack) {
    return stack->index;
}

void Stack_destroy(Stack* stack) {
    free(stack->base);
    free(stack);
}
