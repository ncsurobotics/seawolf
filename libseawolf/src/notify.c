
#include "seawolf.h"

#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

/* Networking includes */
#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/socket.h>

#define FILTER_INCREMENT 5

/* Filter lists */
static bool initialized = false;
static char** filters = NULL;
static int filters_n = 0;
static Queue* notification_queue;
static bool default_policy = NOTIFY_POLICY_DROP;

static bool Notify_check_filter(char* msg);

/**
 * Initialize notify component
 */
void Notify_init() {
    /* Initialize filter list */
    filters = malloc(FILTER_INCREMENT * sizeof(char*));
    notification_queue = Queue_new();
    initialized = true;
} 

/**
 * Close initialize component
 */
void Notify_close() {
    if(!initialized) {
        return;
    }

    char* msg;

    /* Free each filter string */
    for(int i = 0; i < filters_n; i++) {
        free(filters[i]);
    }

    /* Free the filters arrays */
    free(filters);

    /* Free remaining messages */
    while((msg = Queue_pop(notification_queue, false)) != NULL) {
        free(msg);
    }
    Queue_destroy(notification_queue);
}

/**
 * Set policy for accepting messages when not filters exist. By default, all
 * messages are dropped.
 */
void Notify_setPolicy(bool policy) {
    default_policy = policy;
}

/**
 * New message into the queue
 */
void Notify_inputMessage(Comm_Message* message) {
    char* msg = message->components[2];

    if(initialized && Notify_check_filter(msg)) {
        Queue_append(notification_queue, strdup(msg));
    }

    Comm_Message_destroyUnpacked(message);
}

/**
 * Get a message
 */
void Notify_get(char* action, char* param) {
    char* msg;
    char* tmp;

    /* Read message */
    do {
        msg = Queue_pop(notification_queue, true);
    } while(!Notify_check_filter(msg));

    /* Split message */
    tmp = msg;
    while(*tmp != ' ') {
        tmp++;
    }
    *tmp = '\0';

    /* Copy components */
    if(action != NULL) {
        strcpy(action, msg);
    }
    if(param != NULL) {
        strcpy(param, tmp + 1);
    }

    free(msg);
}

/**
 * Send a message
 */
void Notify_send(char* action, char* param) {
    static char* namespace = "NOTIFY";
    static char* command = "OUT";
    Comm_Message* notify_msg = Comm_Message_new(3);

    notify_msg->components[0] = namespace;
    notify_msg->components[1] = command;
    notify_msg->components[2] = strdup(__Util_format("%s %s", action, param));

    Comm_sendMessage(notify_msg);

    free(notify_msg->components[2]);
    Comm_Message_destroy(notify_msg);
}

/**
 * Check a message to determine if it passes through the stored filters 
 */
static bool Notify_check_filter(char* msg) {
    bool match;
    int msg_len;
    char type;
    char* filter;
    int filter_len;

    /* No filters, return policy (default false) */
    if(filters_n == 0) {
        return default_policy;
    }

    msg_len = strlen(msg);
    for(int i = 0; i < filters_n; i++) {
        /* Extract the filter type from the first index of the current filter */
        type = filters[i][0];
        filter = filters[i] + 1;
        filter_len = strlen(filter);

        match = true;

        switch(type) {
         case FILTER_MATCH:
            /* Full text match */
            if(strcmp(filter, msg) == 0) {
                return true;
            }
            break;

         case FILTER_ACTION:
            /* Action match */
            if(msg_len <= filter_len || msg[filter_len] != ' ') {
                match = false;
                break;
            }
            for(int j = 0; j < filter_len; j++) {
                if(msg[j] != filter[j]) {
                    match = false;
                    break;
                }
            }
            if(match) {
                return true;
            }
            break;

         case FILTER_PREFIX:
            /* Prefix match */
            if(filter_len > msg_len) {
                match = false;
                break;
            }
            for(int j = 0; j < filter_len; j++) {
                if(msg[j] != filter[j]) {
                    match = false;
                    break;
                }
            }
            if(match) {
                return true;
            }
            break;
        }
    }

    /* No matches */
    return false;
}

/**
 * Add a new filter. Give a null value to clear filter list
 */
void Notify_filter(int filter_type, char* filter) {
    if(filter == NULL) {
        /* Clear out standard filters */
        for(int i = 0; i < filters_n; i++) {
            /* Free filters */
            free(filters[i]);
        }

        /* Realloc */
        free(filters);
        filters = malloc(FILTER_INCREMENT * sizeof(char*));
        filters_n = 0;

        return;
    }
    
    /* Ran out of room for filters. Increase space */
    if(filters_n && (filters_n % FILTER_INCREMENT) == 0) {
        filters = realloc(filters, (filters_n + FILTER_INCREMENT) * sizeof(char*));
    }

    /* Filters are stored with the filter type stored in the zero index and an
       additional character at the end for the null terminator */
    filters[filters_n] = malloc(sizeof(char) * (strlen(filter) + 2));

    /* Copy in type and filter */
    filters[filters_n][0] = (char) filter_type;
    strcpy(filters[filters_n] + 1, filter);

    /* Increment filter count */
    filters_n++;
}
