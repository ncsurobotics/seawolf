
#include "seawolf.h"

#include <assert.h>
#include <stdlib.h>

List* List_new(void) {
    List* list = malloc(sizeof(List));
    
    if(list == NULL) {
        return NULL;
    }
    
    list->base = (void**) malloc(sizeof(void*) * _LIST_BLOCK_SIZE);
    if(list->base == NULL) {
        free(list);
        return NULL;
    }

    list->space = _LIST_BLOCK_SIZE;
    list->items = 0;
    return list;
}

void List_insert(List* list, void* v, int n) {
    /* Allocation is full so we must expand it */
    if(list->items == list->space) {
        list->space += _LIST_BLOCK_SIZE;
        list->base = realloc(list->base, sizeof(void*) * list->space);
    }

    /* Move all items past the insertion point down one place */
    for(int i = list->items; i > n; i--) {
        list->base[i] = list->base[i-1];
    }
    
    list->base[n] = v;
    list->items++;
}

int List_append(List* list, void* v) {
    List_insert(list, v, list->items);
    return list->items - 1;
}

void List_set(List* list, void* v, int n) {
    if(n < list->items) {
        list->base[n] = v;
    }
}

void* List_get(List* list, int n) {
    if(n < list->items) {
        return list->base[n];
    } else {
        return NULL;
    }
}

void* List_remove(List* list, int n) {
    void* v = List_get(list, n);

    /* Invalid index */
    if(v == NULL) {
        return NULL;
    }

    /* Move items back up the list */
    list->items--;
    for(int i = n; i < list->items; i++) {
        list->base[i] = list->base[i+1];
    }

    /* Shrink the allocation */
    if(list->space - list->items > _LIST_BLOCK_SIZE) {
        list->space -= _LIST_BLOCK_SIZE;
        list->base = realloc(list->base, sizeof(void*) * list->space);
    }

    return v;
}

int List_indexOf(List* list, void* v) {
    for(int i = 0; i < list->items; i++) {
        if(List_get(list, i) == v) {
            return i;
        }
    }
    
    return -1;
}

int List_getSize(List* list) {
    return list->items;
}

List* List_copy(List* list) {
    List* new_list = malloc(sizeof(List));

    if(new_list == NULL) {
        return NULL;
    }
    
    new_list->items = list->items;
    new_list->space = list->space;

    /* Allocate new space */
    new_list->base = malloc(sizeof(void*) * list->space);
    if(new_list->base == NULL) {
        free(new_list);
        return NULL;
    }
    
    memcpy(new_list->base, list->base, sizeof(void*) * list->space);
    return new_list;
}

int List_compareString(void* _s1, void* _s2) {
    char* s1 = _s1;
    char* s2 = _s2;
    return strcmp(s1, s2);
}

int List_compareInt(void* _n1, void* _n2) {
    int *n1 = _n1;
    int *n2 = _n2;
    return (*n1) - (*n2);
}

void List_sort(List* list, int (*cmp)(void*, void*)) {
    if(List_getSize(list) < 2) {
        return;
    }

    List* less = List_new();
    List* more = List_new();
    size_t list_size = List_getSize(list);
    size_t less_size;
    size_t more_size;
    void* reference = List_get(list, 0);
    void* current;

    /* Split list */
    for(int i = 1; i < list_size; i++) {
        current = List_get(list, i);
        if(cmp(reference, current) > 0) {
            List_append(less, current);
        } else {
            List_append(more, current);
        }
    }

    /* Get part sizes */
    less_size = List_getSize(less);
    more_size = List_getSize(more);

    /* Sort parts */
    List_sort(less, cmp);
    List_sort(more, cmp);

    /* Move parts to original */
    memcpy(list->base, less->base, sizeof(void*) * less_size);
    memcpy(list->base + less_size + 1, more->base, sizeof(void*) * more_size);
    list->base[less_size] = reference;
    
    /* Destroy parts */
    List_destroy(less);
    List_destroy(more);
}

void List_destroy(List* list) {
    free(list->base);
    free(list);
}
