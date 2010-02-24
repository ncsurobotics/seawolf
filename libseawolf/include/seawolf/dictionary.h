 
#ifndef __SEAWOLF_DICTIONARY_INCLUDE_H
#define __SEAWOLF_DICTIONARY_INCLUDE_H

#include <stdint.h>

#include <pthread.h>

/* This value should be a power of 2 less than or equal to 32. This will affect
   the granularity of memory allocation but will inversely affect the
   insert/retrieval performance such that it is log(n) with base
   _DICTIONARY_NODE_BITS.  e.g. The higher this value is the faster the tree
   will be, but making it higher will make it less memory efficient. 8 is a good
   value. */
#define _DICTIONARY_NODE_BITS 8

typedef uint32_t hash_t;
#define _DICTIONARY_NODE_SIZE (2 << (_DICTIONARY_NODE_BITS - 1))
#define _DICTIONARY_TREE_DEPTH ((sizeof(hash_t) * 8) / _DICTIONARY_NODE_BITS)
#define _DICTIONARY_HASH_INDEX(hash, i) ((hash_t)(((hash) >> (_DICTIONARY_NODE_BITS * (i))) & (_DICTIONARY_NODE_SIZE - 1)))

typedef enum {
    INTERIOR,
    EXTERIOR
} Dictionary_NodeType;

struct Dictionary_Item_s {
    void* k;
    size_t k_size;
    void* v;
};

struct Dictionary_Node_s {
    int t;
    Dictionary_NodeType nodetype;
    List* active_branches;
    void* branches[_DICTIONARY_NODE_SIZE];
};

struct Dictionary_s {
    struct Dictionary_Node_s* root;
    pthread_mutex_t lock;
    pthread_cond_t new_item;
};

typedef struct Dictionary_Item_s Dictionary_Item;
typedef struct Dictionary_s Dictionary;
typedef struct Dictionary_Node_s Dictionary_Node;

hash_t Dictionary_hash(const void* s, size_t n);

Dictionary* Dictionary_new(void);
void Dictionary_destroy(Dictionary* dict);
List* Dictionary_getKeys(Dictionary* dict);

void Dictionary_setData(Dictionary* dict, const void* k, size_t k_size, void* v);
void Dictionary_setInt(Dictionary* dict, int i, void* v);
void Dictionary_set(Dictionary* dict, const char* k, void* v);

void* Dictionary_getData(Dictionary* dict, const void* k, size_t k_size);
void* Dictionary_getInt(Dictionary* dict, int k);
void* Dictionary_get(Dictionary* dict, const char* k);

void Dictionary_waitForData(Dictionary* dict, const void* k, size_t k_size);
void Dictionary_waitForInt(Dictionary* dict, int k);
void Dictionary_waitFor(Dictionary* dict, const char* k);

bool Dictionary_existsData(Dictionary* dict, const void* k, size_t k_size);
bool Dictionary_existsInt(Dictionary* dict, int k);
bool Dictionary_exists(Dictionary* dict, const char* k);

int Dictionary_removeData(Dictionary* dict, const void* k, size_t k_size);
int Dictionary_removeInt(Dictionary* dict, int k);
int Dictionary_remove(Dictionary* dict, const char* k);

#endif // #ifndef __SEAWOLF_DICTIONARY_INCLUDE_H
