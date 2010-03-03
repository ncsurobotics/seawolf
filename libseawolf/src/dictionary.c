/**
 * \file
 * \brief Dictionary/hash map
 */

#include "seawolf.h"

static void Dictionary_destroyHelper(Dictionary_Node* dn);
static List* Dictionary_getBucket(Dictionary* dict, hash_t hash, bool create);
static int Dictionary_findInBucket(List* bucket, const void* k, size_t k_size);
static Dictionary_Item* Dictionary_getItem(Dictionary* dict, const void* k, size_t k_size);
static Dictionary_Item* Dictionary_Item_new(const void* k, size_t k_size, void* v);
static void Dictionary_Item_destroy(Dictionary_Item* di);
static Dictionary_Node* Dictionary_Node_new(Dictionary_NodeType nodetype);
static void Dictionary_Node_destroy(Dictionary_Node* dn);

/**
 * \defgroup Dictionary Dictionary
 * \ingroup DataStructures
 * \brief Provides a hash map data structure, often known as a dictionary
 * \sa http://en.wikipedia.org/wiki/Hash_map
 * \{
 */

/**
 * \brief Hash a block of memory
 *
 * Return a hash code of the give memory space
 *
 * \param s Pointer to the beginning of the memory space
 * \param n Bytes to include in the hash
 * \return The hash of the given space
 */
hash_t Dictionary_hash(const void* s, size_t n) {
    hash_t hash = 5381;

    for(size_t i = 0; i < n; i++) {
        hash = ((hash << 5) + hash) + ((uint8_t*)s)[i];
    }

    return hash;
}

/**
 * \brief Create a new dictionary
 *
 * Return a new, empty dictionary
 *
 * \return New dictionary
 */
Dictionary* Dictionary_new(void) {
    Dictionary* dict = malloc(sizeof(Dictionary));
    if(dict == NULL) {
        return NULL;
    }

    dict->root = Dictionary_Node_new(INTERIOR);
    if(dict->root == NULL) {
        free(dict);
        return NULL;
    }

    pthread_mutex_init(&dict->lock, NULL);
    pthread_cond_init(&dict->new_item, NULL);

    return dict;
}

/**
 * \brief Retrieve the bucket for a hash
 *
 * Each hash code resolves to a bucket at the edge of the tree. This function
 * finds, possibly creates, and returns a reference to this bucket
 *
 * \param dict The dictionary to search in
 * \param has The hash to use for the lookup
 * \param create If true, the bucket will be created if it doesn't exist as well
 * as any intermediate nodes needed. If false, NULL will be returned if the
 * bucket is not found
 * \return The bucket, or NULL if \a create if false and the bucket could not be
 * found
 */
static List* Dictionary_getBucket(Dictionary* dict, hash_t hash, bool create) {
    Dictionary_Node* dn = dict->root;
    hash_t hash_part;
    List* bucket;

    for(int i = 0; i < _DICTIONARY_TREE_DEPTH - 1; i++) {
        hash_part = _DICTIONARY_HASH_INDEX(hash, i);
        if(dn->branches[hash_part] == NULL) {
            if(create) {
                if(i < _DICTIONARY_TREE_DEPTH - 2) {
                    dn->branches[hash_part] = Dictionary_Node_new(INTERIOR);
                } else {
                    dn->branches[hash_part] = Dictionary_Node_new(EXTERIOR);
                }
                List_append(dn->active_branches, dn->branches[hash_part]);
            } else {
                return NULL;
            } 
        }
        dn = dn->branches[hash_part];
    }

    hash_part = _DICTIONARY_HASH_INDEX(hash, _DICTIONARY_TREE_DEPTH - 1);
    if(dn->branches[hash_part] == NULL) {
        if(create) {
            dn->branches[hash_part] = List_new();
            List_append(dn->active_branches, dn->branches[hash_part]);
        } else {
            return NULL;
        }
    }

    bucket = dn->branches[hash_part];
    return bucket;
}

/**
 * \brief Set an element
 *
 * Set an element in the dictionary
 *
 * \param dict The dictionary to set for
 * \param k The generic key
 * \param k_size The generic key size
 * \param v The value to set
 */
void Dictionary_setData(Dictionary* dict, const void* k, size_t k_size, void* v) {
    Dictionary_Item* di_new;
    Dictionary_Item* di_temp;
    hash_t hash = Dictionary_hash(k, k_size);
    List* bucket;
    size_t bucket_size;

    pthread_mutex_lock(&dict->lock);

    bucket = Dictionary_getBucket(dict, hash, true);
    bucket_size = List_getSize(bucket);
    for(int i = 0; i < bucket_size; i++) {
        di_temp = List_get(bucket, i);
        if(memcmp(k, di_temp->k, k_size) == 0) {
            /* Update existing */
            di_temp->v = v;
            goto release_locks;
        }
    }

    di_new = Dictionary_Item_new(k, k_size, v);
    List_append(bucket, di_new);

 release_locks:
    pthread_cond_broadcast(&dict->new_item);
    pthread_mutex_unlock(&dict->lock);
}

/**
 * \brief Set an element
 *
 * Set an element in the dictionary
 *
 * \param dict The dictionary to set for
 * \param i The integer key
 * \param v The value to set
 */
void Dictionary_setInt(Dictionary* dict, int i, void* v) {
    Dictionary_setData(dict, &i, sizeof(int), v);
}

/**
 * \brief Set an element
 *
 * Set an element in the dictionary
 *
 * \param dict The dictionary to set for
 * \param k The string key
 * \param v The value to set
 */
void Dictionary_set(Dictionary* dict, const char* k, void* v) {
    Dictionary_setData(dict, k, strlen(k) + 1, v);
}

/**
 * \brief Locate a key in a bucket
 *
 * Each hash code maps to a particular bucket in the tree. This function locates
 * a actual key within this bucket
 *
 * \param list The bucket to search
 * \param k The key to search for
 * \param k_size The size/length of the key
 * \return The index of the item in the bucket, or -1 if the item is not found
 */
static int Dictionary_findInBucket(List* bucket, const void* k, size_t k_size) {
    Dictionary_Item* di;
    size_t bucket_size;
 
    /* Find key in bucket */
    bucket_size = List_getSize(bucket);
    for(int i = 0; i < bucket_size; i++) {
        di = List_get(bucket, i);
        if(memcmp(k, di->k, k_size) == 0) {
            /* Key found */
            return i;
        }
    }

    return -1;
}

/**
 * \brief Retrieve an item object from a dictionary
 *
 * Get the item associated with the given key
 *
 * \param dict The dictionary to retrieve from
 * \param k The key to locate
 * \param k_size The size/length of the key
 * \return The Dictionary_Item associated with the key, or NULL if the key was
 * not found
 */
static Dictionary_Item* Dictionary_getItem(Dictionary* dict, const void* k, size_t k_size) {
    hash_t hash = Dictionary_hash(k, k_size);
    List* bucket;
    int bucket_index;
    void* v = NULL;

    bucket = Dictionary_getBucket(dict, hash, false);
    if(bucket != NULL) {
        bucket_index = Dictionary_findInBucket(bucket, k, k_size);
        if(bucket_index != -1) {
            v = List_get(bucket, bucket_index);;
        }
    }

    return v;
}

/**
 * \brief Retrieve an element
 *
 * Retrieve an element from the dictionary
 *
 * \param dict The dictionary to retrieve from
 * \param k The generic key
 * \param k_size The generic key size
 * \return The value associated with the key or NULL if the key is not found
 */
void* Dictionary_getData(Dictionary* dict, const void* k, size_t k_size) {
    Dictionary_Item* di;

    pthread_mutex_lock(&dict->lock);
    di = Dictionary_getItem(dict, k, k_size);
    pthread_mutex_unlock(&dict->lock);

    if(di == NULL) {
        /* Invalid key */
        return NULL;
    }

    return di->v;
}

/**
 * \brief Retrieve an element
 *
 * Retrieve an element from the dictionary
 *
 * \param dict The dictionary to retrieve from
 * \param k The integer key
 * \return The value associated with the key or NULL if the key is not found
 */
void* Dictionary_getInt(Dictionary* dict, int k) {
    return Dictionary_getData(dict, &k, sizeof(int));
}

/**
 * \brief Retrieve an element
 *
 * Retrieve an element from the dictionary
 *
 * \param dict The dictionary to retrieve from
 * \param k The string key
 * \return The value associated with the key or NULL if the key is not found
 */
void* Dictionary_get(Dictionary* dict, const char* k) {
    return Dictionary_getData(dict, k, strlen(k) + 1);
}

/**
 * \brief Wait for a key to enter the dictionary
 *
 * Wait for a generic key to be in the dictionary
 *
 * \param dict The dictionary to wait on
 * \param k The generic key to wait on
 * \param k_size The generic key size
 */
void Dictionary_waitForData(Dictionary* dict, const void* k, size_t k_size) {
    pthread_mutex_lock(&dict->lock);
    while(Dictionary_getItem(dict, k, k_size) == NULL) {
        pthread_cond_wait(&dict->new_item, &dict->lock);
    }
    pthread_mutex_unlock(&dict->lock);
}

/**
 * \brief Wait for a key to enter the dictionary
 *
 * Wait for an integer key to be in the dictionary
 *
 * \param dict The dictionary to wait on
 * \param k The integer key to wait on
 */
void Dictionary_waitForInt(Dictionary* dict, int k) {
    Dictionary_waitForData(dict, &k, sizeof(int));
}

/**
 * \brief Wait for a key to enter the dictionary
 *
 * Wait for a string key to be in the dictionary
 *
 * \param dict The dictionary to wait on
 * \param k The string key to wait on
 */
void Dictionary_waitFor(Dictionary* dict, const char* k) {
    Dictionary_waitForData(dict, k, strlen(k) + 1);
}

/**
 * \brief Check if a key is in the dictionary
 *
 * Check if the generic key exists in the dictionary
 *
 * \param dict The dictionary to check
 * \param k The generic key
 * \param k_size The generic key length
 * \return true if the key exists, false otherwise
 */
bool Dictionary_existsData(Dictionary* dict, const void* k, size_t k_size) {
    /* If a Dictionary_Item does not exist for the key then return false */
    Dictionary_Item* di;
    
    pthread_mutex_lock(&dict->lock);
    di = Dictionary_getItem(dict, k, k_size);
    pthread_mutex_unlock(&dict->lock);

    if(di == NULL) {
        return false;
    }
    
    /* Key exists */
    return true;
}

/**
 * \brief Check if a key is in the dictionary
 *
 * Check if the integer key exists in the dictionary
 *
 * \param dict The dictionary to check
 * \param k The integer key
 * \return true if the key exists, false otherwise
 */
bool Dictionary_existsInt(Dictionary* dict, int k) {
    return Dictionary_existsData(dict, &k, sizeof(k));
}

/**
 * \brief Check if a key is in the dictionary
 *
 * Check if the string key exists in the dictionary
 *
 * \param dict The dictionary to check
 * \param k The string key
 * \return true if the key exists, false otherwise
 */
bool Dictionary_exists(Dictionary* dict, const char* k) {
    return Dictionary_existsData(dict, k, strlen(k) + 1);
}

/**
 * \brief Remove a dictionary element
 *
 * Remove an element from the dictionary associated with the generic key
 *
 * \param dict The dictionary to remove from
 * \param k The generic key
 * \param k_size Length of the key
 * \return -1 in the remove failed. 0 if successful
 */
int Dictionary_removeData(Dictionary* dict, const void* k, size_t k_size) {
    hash_t hash = Dictionary_hash(k, k_size);
    List* bucket;
    int bucket_index;
    int ret = -1;

    pthread_mutex_lock(&dict->lock);

    bucket = Dictionary_getBucket(dict, hash, false);
    if(bucket != NULL) {
        bucket_index = Dictionary_findInBucket(bucket, k, k_size);
        if(bucket_index != -1) {
            Dictionary_Item_destroy(List_remove(bucket, bucket_index));
            ret = 0;
        }
    }

    pthread_mutex_unlock(&dict->lock);
    return ret;
}

/**
 * \brief Remove a dictionary element
 *
 * Remove an element from the dictionary associated with the integer key
 *
 * \param dict The dictionary to remove from
 * \param k The integer key
 * \return -1 in the remove failed. 0 if successful
 */
int Dictionary_removeInt(Dictionary* dict, int k) {
    return Dictionary_removeData(dict, &k, sizeof(int));
}

/**
 * \brief Remove a dictionary element
 *
 * Remove an element from the dictionary associated with the string key
 *
 * \param dict The dictionary to remove from
 * \param k The string key
 * \return -1 in the remove failed. 0 if successful
 */
int Dictionary_remove(Dictionary* dict, const char* k) {
    return Dictionary_removeData(dict, k, strlen(k) + 1);
}

/**
 * \brief Helper for Dictionary_getKeys()
 *
 * Recrusively retrieve all keys from the dictionary
 *
 * \param dn The root dictionary node
 * \return A list of the dictionary's keys
 */
static List* Dictionary_getKeysHelper(Dictionary_Node* dn) {
    Dictionary_Node* dn_temp;
    int active_branch_count = List_getSize(dn->active_branches);
    List* keys = List_new();
    List* temp_keys;
    List* bucket;
    int size;

    if(dn->nodetype == EXTERIOR) {
        for(int i = 0; i < active_branch_count; i++) {
            bucket = List_get(dn->active_branches, i);
            size = List_getSize(bucket);
            for(int j = 0; j < size; j++) {
                List_append(keys, ((Dictionary_Item*)List_get(bucket, j))->k);
            }
        }
    } else {
        for(int i = 0; i < active_branch_count; i++) {
            dn_temp = List_get(dn->active_branches, i);
            temp_keys = Dictionary_getKeysHelper(dn_temp);
            size = List_getSize(temp_keys);
            for(int j = 0; j < size; j++) {
                List_append(keys, List_get(temp_keys, j));
            }
            List_destroy(temp_keys);
        }
    }

    return keys;
}

/**
 * \brief Get the list of keys
 *
 * Return pointers to all the keys in the dictionary. The keys should not be freed
 *
 * \param dict The list to retrieve keys for
 * \return List of the keys
 */
List* Dictionary_getKeys(Dictionary* dict) {
    return Dictionary_getKeysHelper(dict->root);
}

/**
 * \brief Create a new dictionary item
 *
 * Create a new dictionary item
 *
 * \param k The item key
 * \param k_size The size/length of the item key
 * \param v The value to store in the item
 * \return A new item object
 */
static Dictionary_Item* Dictionary_Item_new(const void* k, size_t k_size, void* v) {
    Dictionary_Item* di = malloc(sizeof(Dictionary_Item));

    if(di == NULL) {
        return NULL;
    }

    di->k = malloc(k_size);
    di->k_size = k_size;
    di->v = v;

    memcpy(di->k, k, k_size);

    return di;
}

/**
 * \brief Destroy a dictionary item object
 *
 * Destroy a dictionary item object
 *
 * \param di The item to destroy
 */
static void Dictionary_Item_destroy(Dictionary_Item* di) {
    free(di->k);
    free(di);
}

/**
 * \brief Create a new node
 *
 * Create a new node
 *
 * \param nodetype The type of the node
 * \return A new node
 */
static Dictionary_Node* Dictionary_Node_new(Dictionary_NodeType nodetype) {
    Dictionary_Node* dn = malloc(sizeof(Dictionary_Node));
    if(dn == NULL) {
        return NULL;
    }
    
    dn->nodetype = nodetype;
    dn->active_branches = List_new();

    for(int i = 0; i < _DICTIONARY_NODE_SIZE; i++) {
        dn->branches[i] = NULL;
    }
    
    return dn;
}

/**
 * \brief Destroy a dictionary node
 *
 * Destroy a dictionary node
 *
 * \param dn The node to destroy
 */
static void Dictionary_Node_destroy(Dictionary_Node* dn) {
    List_destroy(dn->active_branches);
    free(dn);
}

/**
 * \brief Helper for Dictionary_destroy()
 *
 * Recursively destroys the dictionary tree, freeing all memory allocated to it
 *
 * \param dn Root dictionary node
 */
static void Dictionary_destroyHelper(Dictionary_Node* dn) {
    Dictionary_Node* dn_next = NULL;
    int active_branch_count = 0;

    List* bucket = NULL;
    int bucket_size = 0;

    active_branch_count = List_getSize(dn->active_branches);

    for(int i = 0; i < active_branch_count; i++) {
        if(dn->nodetype == INTERIOR) {
            dn_next = List_get(dn->active_branches, i);
            Dictionary_destroyHelper(dn_next);
        } else {
            bucket = List_get(dn->active_branches, i);
            bucket_size = List_getSize(bucket);
            for(int j = 0; j < bucket_size; j++) {
                Dictionary_Item_destroy(List_get(bucket, j));
            }
            List_destroy(bucket);
        }
    }

    Dictionary_Node_destroy(dn);
}

/**
 * \brief Destroy a dictionary
 *
 * Free a dictionary
 *
 * \param dict The dictionary to free
 */
void Dictionary_destroy(Dictionary* dict) {
    Dictionary_destroyHelper(dict->root);
    free(dict);
}

/** \} */
