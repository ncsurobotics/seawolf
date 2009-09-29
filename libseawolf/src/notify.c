
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

/* IO Mode. Default to net */
static int io_mode = NOTIFY_NET;
//static int io_mode = NOTIFY_STDIO;

/* Server name. localhost by default */
static char server_hostname[256] = "localhost";

/* Filter lists */
static char** filters = NULL;
static int filters_n = 0;

/* Raw send messages */
static void Notify_real_send_net(char* data);
static void Notify_real_send_stdio(char* data);
static void Notify_real_get_net(char* data);
static void Notify_real_get_stdio(char* data);
static bool Notify_check_filter(char* msg);

/* Server connection */
static int connection = -1;

/* Message lock */
static pthread_mutex_t* send_lock = NULL;
static pthread_mutex_t* recv_lock = NULL;

/**
 * Initialize notify component
 */
void Notify_init() {
    struct hostent* host;
    struct sockaddr_in host_sockaddr;
    char* ipaddr_s;

    /* Initialize send and receive locks */
    send_lock = malloc(sizeof(pthread_mutex_t));
    recv_lock = malloc(sizeof(pthread_mutex_t));    pthread_mutexattr_t attr;
    pthread_mutexattr_init(&attr);
    pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_RECURSIVE);
    pthread_mutex_init(send_lock, &attr);
    pthread_mutex_init(recv_lock, &attr);
    pthread_mutexattr_destroy(&attr);

    /* Initialize filter list */
    filters = malloc(FILTER_INCREMENT * sizeof(char*));

    /* Connect to the notify "hub" server if net mode is enabled */
    if(io_mode == NOTIFY_NET) {
        /* New socket */
        connection = socket(AF_INET, SOCK_STREAM, 0);
        if(connection == -1) {
            fprintf(stderr, "Error creating socket: %s\nExiting\n", strerror(errno));
            exit(1);
        }
        
        /* Get IP address of host */
        host = gethostbyname(server_hostname);
        ipaddr_s = host->h_addr_list[0];

        /* Build sockaddr structure */
        host_sockaddr.sin_family = AF_INET;
        host_sockaddr.sin_addr.s_addr = *(int*)ipaddr_s;
        host_sockaddr.sin_port = htons(NET_PORT);

        /* Connect */
        if(connect(connection, (struct sockaddr*) &host_sockaddr, sizeof(host_sockaddr)) == -1) {
            fprintf(stderr, "Could not connect to hub/repeater server: %s\nExiting\n", strerror(errno));
            exit(1);
        }
    }
} 

/**
 * Close initialize component
 */
void Notify_close() {
    /* Free each filter string */
    for(int i = 0; i < filters_n; i++) {
        free(filters[i]);
    }

    /* Free the filters arrays */
    free(filters);

    if(io_mode == NOTIFY_NET) {
        /* Close connection */
        shutdown(connection, SHUT_RDWR);
        connection = -1;
    }

    /* Free locks */
    pthread_mutex_destroy(send_lock);
    pthread_mutex_destroy(recv_lock);
    free(send_lock);
    free(recv_lock);
}

/**
 * Set IO mode. Should *not* be called after initialization
 */
void Notify_setMode(int mode) {
    io_mode = mode;
}

/**
 * Set server address of notify "hub" server. Should *not* be called after
 * initialization
 */
void Notify_setServer(char* hostname) {
    /* Copy server name */
    strcpy(server_hostname, hostname);
}

/**
 * Get a raw message
 */
void Notify_getRaw(char* message) {
    /* Received messages from the correct IO methods until a valid messages is
       found */
    switch(io_mode) {
     case NOTIFY_NET:
        do {
            Notify_real_get_net(message);
        } while(! Notify_check_filter(message));
        break;

     case NOTIFY_STDIO:
        do {
            Notify_real_get_stdio(message);
        } while(! Notify_check_filter(message));
        break;

     default:
        break;
    }
}

/**
 * Get a message
 */
void Notify_get(char* action, char* param) {
    char msg[MAX_MESSAGE_LENGTH];
    char* tmp;

    /* Read message */
    Notify_getRaw(msg);

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
}

/**
 * Send a raw message
 */
void Notify_sendRaw(char* message) {
    switch(io_mode) {
     case NOTIFY_NET:
        Notify_real_send_net(message);
        break;

     case NOTIFY_STDIO:
        Notify_real_send_stdio(message);
        break;

     default:
        break;
    }
}

/**
 * Send a message
 */
void Notify_send(char* action, char* param) {
    char buffer[MAX_MESSAGE_LENGTH];
    sprintf(buffer, "%s %s", action, param);
    Notify_sendRaw(buffer);
}

/**
 * Send a message over the network
 */
static void Notify_real_send_net(char* data) {
    pthread_mutex_lock(send_lock);
    int size = strlen(data) + 1;
    int sent;
    
    /* Send until all the input is sent */
    while(size) {
        sent = send(connection, data, size, 0);
        if(sent == -1) {
            /* Error condition */
            perror("Error sending message, giving up");
            return;
        }
        size -= sent;
        data += sent;
    }
    pthread_mutex_unlock(send_lock);
}

/**
 * Send a message out over standard output
 */
static void Notify_real_send_stdio(char* data) {
    pthread_mutex_lock(send_lock);
    printf("%s\n", data);
    pthread_mutex_unlock(send_lock);
}

/**
 * Get a message from the network
 */
static void Notify_real_get_net(char* data) {
    pthread_mutex_lock(recv_lock);
    /* Read one character at a time until a null terminator */
    while(true) {
        if(recv(connection, data, sizeof(char), 0) == -1) {
            perror("Error receiving message, giving up");
            return;
        }
        if(*data == '\0') {
            return;
        }
        data++;
    }
    pthread_mutex_unlock(recv_lock);
}

/**
 * Get a message from the standard input
 */
static void Notify_real_get_stdio(char* data) {
    pthread_mutex_lock(recv_lock);
    /* Read characters until a new line */
    while(true) {
        *data = getchar();
        if(*data == '\n') {
            break;
        }
        data++;
    }
    *data = '\0';
    pthread_mutex_unlock(recv_lock);
}

/**
 * Check a message to determine if it passes through the stored filters 
 */
static bool Notify_check_filter(char* msg) {
    bool match;
    int msg_len = strlen(msg);
    
    char type;
    char* filter;
    int filter_len;

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

    /* No matches or no filters; return true if no filters */
    return (filters_n == 0);
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
