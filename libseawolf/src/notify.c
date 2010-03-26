/**
 * \file
 * \brief Notification support
 */

#include "seawolf.h"

/**
 * Amount by which to increment the filter space
 * \private
 */
#define FILTER_INCREMENT 5

/** True if the notify component has been initialized */
static bool initialized = false;

/** List of fitlers */
static char** filters = NULL;

/** Number of registered filters */
static int filters_n = 0;

/** Queue of buffered, incoming messages */
static Queue* notification_queue;

/** Default policy for messages when no filters are in place */
static bool default_policy = NOTIFY_POLICY_DROP;

static bool Notify_check_filter(char* msg);

/**
 * \defgroup Notify Notifications (broadcast messages)
 * \ingroup Communications
 * \brief Notify related routines
 * \{
 */

/**
 * \brief Initialize notify component
 * \private
 */
void Notify_init() {
    /* Initialize filter list */
    filters = malloc(FILTER_INCREMENT * sizeof(char*));
    notification_queue = Queue_new();
    initialized = true;
} 

/**
 * \brief Set accept policy
 *
 * Set policy for accepting messages when not filters exist. By default, all
 * messages are dropped.
 *
 * \param policy Accept by default if true, deny by default if false
 */
void Notify_setPolicy(bool policy) {
    default_policy = policy;
}

/**
 * \brief Input a new message
 * \internal
 *
 * Provide a new message for the incoming notification queue
 * 
 * \param message New message
 */
void Notify_inputMessage(Comm_Message* message) {
    char* msg = message->components[2];

    if(initialized && Notify_check_filter(msg)) {
        Queue_append(notification_queue, strdup(msg));
    }

    Comm_Message_destroyUnpacked(message);
}

/**
 * \brief Get next message
 *
 * Get the next notification message available
 *
 * \param[out] action Pointer into which to store the notification action
 * \param[out] param Pointer into which to store the notification parameter
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
 * \brief Send a notification
 *
 * Send out a notification
 *
 * \param action Action component of notification
 * \param param Parameter component of notification
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
 * \brief Filter a message
 *
 * Check a message to determine if it passes through the stored filters 
 *
 * \param msg The message to check
 * \return True if the message matches a filter, false otherwise
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
 * \brief Register a new filter
 * 
 * Register a new filter with the notification system. Incoming messages must
 * match a filter in order to be returned by Notify_get(). If no filters are
 * active then messages are accepted or denied based on the accept policy (see
 * Notify_setPolicy()).
 *
 * There are three kinds of filters,
 *  - FILTER_MATCH requires the entire message to match
 *  - FILTER_ACTION requires the action of the message to match
 *  - FILTER_PREFIX requires some sequences of characters at the beginning of the message to match
 *
 * All existing filters can be removed by specifying NULL for the filter
 * argument
 *
 * \param filter_type One of FILTER_MATCH, FILTER_ACTION, or FILTER_PREFIX.
 * \param filter The filter text, applied as described by the filter_type
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

/**
 * \brief Close initialize component
 * \private
 */
void Notify_close() {
    char* msg;

    if(initialized) {
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

        initialized = false;
    }
}

/** \} */
