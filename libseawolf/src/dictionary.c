
#include "seawolf.h"

#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static void Dictionary_destroyHelper(Dictionary_Node* dn);
static List* Dictionary_getBucket(Dictionary* dict, hash_t hash, bool create);
static int Dictionary_findInBucket(List* bucket, const void* k, size_t k_size);
static Dictionary_Item* Dictionary_getItem(Dictionary* dict, const void* k, size_t k_size);
static Dictionary_Item* Dictionary_Item_new(const void* k, size_t k_size, void* v);
static void Dictionary_Item_destroy(Dictionary_Item* di);
static Dictionary_Node* Dictionary_Node_new(Dictionary_NodeType nodetype);
static void Dictionary_Node_destroy(Dictionary_Node* dn);

hash_t Dictionary_hash(const void* s, size_t n) {
    hash_t hash = 5381;

    for(size_t i = 0; i < n; i++) {
        hash = ((hash << 5) + hash) + ((uint8_t*)s)[i];
    }

    return hash;
}

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

void Dictionary_destroy(Dictionary* dict) {
    Dictionary_destroyHelper(dict->root);
    free(dict);
}

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

void Dictionary_setInt(Dictionary* dict, int i, void* v) {
    Dictionary_setData(dict, &i, sizeof(int), v);
}

void Dictionary_set(Dictionary* dict, const char* k, void* v) {
    Dictionary_setData(dict, k, strlen(k) + 1, v);
}

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

void* Dictionary_getInt(Dictionary* dict, int k) {
    return Dictionary_getData(dict, &k, sizeof(int));
}

void* Dictionary_get(Dictionary* dict, const char* k) {
    return Dictionary_getData(dict, k, strlen(k) + 1);
}

void Dictionary_waitForData(Dictionary* dict, const void* k, size_t k_size) {
    pthread_mutex_lock(&dict->lock);
    while(Dictionary_getItem(dict, k, k_size) == NULL) {
        pthread_cond_wait(&dict->new_item, &dict->lock);
    }
    pthread_mutex_unlock(&dict->lock);
}

void Dictionary_waitForInt(Dictionary* dict, int k) {
    Dictionary_waitForData(dict, &k, sizeof(int));
}

void Dictionary_waitFor(Dictionary* dict, const char* k) {
    Dictionary_waitForData(dict, k, strlen(k) + 1);
}

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

bool Dictionary_existsInt(Dictionary* dict, int k) {
    return Dictionary_existsData(dict, &k, sizeof(k));
}

bool Dictionary_exists(Dictionary* dict, const char* k) {
    return Dictionary_existsData(dict, k, strlen(k) + 1);
}

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

int Dictionary_removeInt(Dictionary* dict, int k) {
    return Dictionary_removeData(dict, &k, sizeof(int));
}

int Dictionary_remove(Dictionary* dict, const char* k) {
    return Dictionary_removeData(dict, k, strlen(k) + 1);
}

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

List* Dictionary_getKeys(Dictionary* dict) {
    return Dictionary_getKeysHelper(dict->root);
}

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

static void Dictionary_Item_destroy(Dictionary_Item* di) {
    free(di->k);
    free(di);
}

static Dictionary_Node* Dictionary_Node_new(Dictionary_NodeType nodetype) {
    Dictionary_Node* dn = malloc(sizeof(Dictionary_Node));
    if(dn == NULL) {
        return NULL;
    }
    
    dn->nodetype = nodetype;
    dn->active_branches = List_new();
    dn->t = 5;

    for(int i = 0; i < _DICTIONARY_NODE_SIZE; i++) {
        dn->branches[i] = NULL;
    }
    
    return dn;
}

static void Dictionary_Node_destroy(Dictionary_Node* dn) {
    List_destroy(dn->active_branches);
    free(dn);
}
