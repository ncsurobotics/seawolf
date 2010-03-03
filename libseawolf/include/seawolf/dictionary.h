/**
 * \file
 */
 
#ifndef __SEAWOLF_DICTIONARY_INCLUDE_H
#define __SEAWOLF_DICTIONARY_INCLUDE_H

#include <stdint.h>

#include <pthread.h>

/**
 * This value should be a power of 2 less than or equal to 32. This will affect
 * the granularity of memory allocation but will inversely affect the
 * insert/retrieval performance such that it is log(n) with base
 * _DICTIONARY_NODE_BITS. e.g. The higher this value is the faster the tree will
 * be, but making it higher will make it less memory efficient. 8 is a good
 * value.
 */
#define _DICTIONARY_NODE_BITS 8

/**
 * Typedef for 32 bit hash
 */
typedef uint32_t hash_t;

/**
 * Number of branches per node
 * \private
 */
#define _DICTIONARY_NODE_SIZE (2 << (_DICTIONARY_NODE_BITS - 1))

/**
 * Number of levels in the tree
 * \private
 */
#define _DICTIONARY_TREE_DEPTH ((sizeof(hash_t) * 8) / _DICTIONARY_NODE_BITS)

/**
 * Return the brach index for the given hash at each level i
 * \private
 */
#define _DICTIONARY_HASH_INDEX(hash, i) ((hash_t)(((hash) >> (_DICTIONARY_NODE_BITS * (i))) & (_DICTIONARY_NODE_SIZE - 1)))

/**
 * Gives the position of a node in a dictionary tree
 * \private
 */
typedef enum {
    /**
     * Interior of the tree
     */
    INTERIOR,

    /**
     * At the edge of the tree
     */
    EXTERIOR
} Dictionary_NodeType;

/**
 * An item in a dictionary
 * \private
 */
typedef struct {
    /**
     * Key
     * \private
     */
    void* k;

    /**
     * Key size/length
     * \private
     */
    size_t k_size;

    /**
     * Value
     * \private
     */
    void* v;
} Dictionary_Item;

/**
 * Tree node in the dictionary
 *
 * \private
 */
typedef struct {
    /**
     * Node type
     * \private
     */
    Dictionary_NodeType nodetype;

    /**
     * Branches in the tree which have children
     * \private
     */
    List* active_branches;

    /**
     * Child branches
     * \private
     */
    void* branches[_DICTIONARY_NODE_SIZE];
} Dictionary_Node;

/**
 * Dictionary object
 */
typedef struct {
    /**
     * Root node of the dictionary's tree
     * \private
     */
    Dictionary_Node* root;

    /**
     * Dictionary mutex lock
     * \private
     */
    pthread_mutex_t lock;

    /**
     * New item conditional
     * \private
     */
    pthread_cond_t new_item;
} Dictionary;

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
