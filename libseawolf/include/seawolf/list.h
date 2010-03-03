/**
 * \file
 */
 
#ifndef __SEAWOLF_LIST_INCLUDE_H
#define __SEAWOLF_LIST_INCLUDE_H

/**
 * List
 */
typedef struct {
    /**
     * List space base address
     * \private
     */
    void** base;

    /**
     * Number of items
     * \private
     */
    int items;

    /**
     * Ammount of space
     * \private
     */
    int space;
} List;

List* List_new(void);
void List_insert(List* stack, void* v, int n);
int List_append(List* stack, void* v);
void List_set(List* list, void* v, int n);
void* List_get(List* stack, int n);
void* List_remove(List* stack, int n);
int List_indexOf(List* list, void* v);
int List_getSize(List* stack);
List* List_copy(List* list);
void List_destroy(List* stack);
int List_compareString(void* s1, void* s2);
int List_compareInt(void* n1, void* n2);
void List_sort(List* list, int (*cmp)(void*, void*));

#endif // #ifndef __SEAWOLF_LIST_INCLUDE_H
