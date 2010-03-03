/**
 * \file
 * \brief List
 */

#include "seawolf.h"

/**
 * Amount by which to grow/shrink the list space
 * \private
 */
#define LIST_BLOCK_SIZE 16

/**
 * \defgroup List List
 * \ingroup DataStructures
 * \brief A simple list implementation which automatically grows
 * \sa http://en.wikipedia.org/wiki/List_%28data_structure%29
 * \{
 */

/**
 * \brief Create a new List object
 *
 * Return a new, empty List object
 *
 * \return The new list
 */
List* List_new(void) {
    List* list = malloc(sizeof(List));
    
    if(list == NULL) {
        return NULL;
    }
    
    list->base = (void**) malloc(sizeof(void*) * LIST_BLOCK_SIZE);
    if(list->base == NULL) {
        free(list);
        return NULL;
    }

    list->space = LIST_BLOCK_SIZE;
    list->items = 0;
    return list;
}

/**
 * \brief Insert an item
 *
 * Insert a new item into a list at the given index
 *
 * \param list The list to insert into
 * \param v The item to insert
 * \param n The index to insert v at
 */
void List_insert(List* list, void* v, int n) {
    /* Allocation is full so we must expand it */
    if(list->items == list->space) {
        list->space += LIST_BLOCK_SIZE;
        list->base = realloc(list->base, sizeof(void*) * list->space);
    }

    /* Move all items past the insertion point down one place */
    for(int i = list->items; i > n; i--) {
        list->base[i] = list->base[i-1];
    }
    
    list->base[n] = v;
    list->items++;
}

/**
 * \brief Append an item to the list
 *
 * Insert an item at the end of the list
 *
 * \param list The list to append to
 * \param v The item to append
 * \return The index of the appended item
 */
int List_append(List* list, void* v) {
    List_insert(list, v, list->items);
    return list->items - 1;
}

/**
 * \brief Set an item at an index
 *
 * Set the value of the item at a given index
 *
 * \param list The list to set the item for
 * \param v The new item
 * \param n The index of the list to update
 */
void List_set(List* list, void* v, int n) {
    if(n < list->items) {
        list->base[n] = v;
    }
}

/**
 * \brief Get an item from a list
 *
 * Return the item from list at the given index
 *
 * \param list The list to retrieve from
 * \param n The index in the list to return from
 * \return The item at the given index or NULL if the index is out of bounds
 */
void* List_get(List* list, int n) {
    if(n < list->items) {
        return list->base[n];
    } else {
        return NULL;
    }
}

/**
 * \brief Remove an item from a list
 *
 * Remove the item at the given index from the list
 *
 * \param list The list to remove from
 * \param n The index of the item to remove
 * \return The removed item or NULL in the case of n being out of bounds
 */
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
    if(list->space - list->items > LIST_BLOCK_SIZE) {
        list->space -= LIST_BLOCK_SIZE;
        list->base = realloc(list->base, sizeof(void*) * list->space);
    }

    return v;
}

/**
 * \brief Find an item in the list
 *
 * Find the index of the given item in the list
 *
 * \param list The list to search
 * \param v The item to search for
 * \return The index of the item in the list or -1 otherwise (not found)
 */
int List_indexOf(List* list, void* v) {
    for(int i = 0; i < list->items; i++) {
        if(List_get(list, i) == v) {
            return i;
        }
    }
    
    return -1;
}

/**
 * \brief Get the size of the list
 *
 * Return the number of items in the list
 *
 * \param list The list to return the size of
 * \return The number of items in the list
 */
int List_getSize(List* list) {
    return list->items;
}

/**
 * \brief Copy a list
 *
 * Return a new list with the same items as the given list. Note that the items
 * themselves are not duplicated
 *
 * \param list The list to copy
 * \return A new list, identical to the given list
 */
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

/**
 * \brief String comparitor
 * 
 * A string comparitor
 * \sa List_sort
 *
 * \param _s1 The first string
 * \param _s2 The second string
 * \return The order of _s1 and _s2
 */
int List_compareString(void* _s1, void* _s2) {
    char* s1 = _s1;
    char* s2 = _s2;
    return strcmp(s1, s2);
}

/**
 * \brief Integer comparitor
 * 
 * An integer comparitor
 * \sa List_sort
 *
 * \param _n1 A pointer to the first integer
 * \param _n2 A pointer to the second integer
 * \return The order of _n1 and _n2
 */
int List_compareInt(void* _n1, void* _n2) {
    int *n1 = _n1;
    int *n2 = _n2;
    return (*n1) - (*n2);
}

/**
 * \brief Sort a list
 *
 * Sort a list inplace using the given function as a comparator
 *
 * \sa List_compareString
 * \sa List_compareInt
 *
 * \param list The list to sort
 * \param cmp A function taking two void* and return an int. This function is
 * used to determine the sorting order of the list. cmp(a, b) should return -1
 * if a < b, 1 if a > b and 0 if a = b
 * \return your mom
 */
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

/**
 * \brief Destroy the list
 *
 * Free the list without freeing any memory associated with the elements of the list
 *
 * \param list The list to free
 */
void List_destroy(List* list) {
    free(list->base);
    free(list);
}

/** \} */
