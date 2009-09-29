
#define __SEAWOLF_UTIL__
#include "seawolf.h"

#include <pthread.h>
#include <stdarg.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <ctype.h>
#include <sys/time.h>

#define FORMAT_BUFF_SIZE 256

struct Buffer {
    pthread_t id;
    char buff[FORMAT_BUFF_SIZE];
};

static struct Buffer* format_buffers = NULL;
static int buffer_count = 0;

void Util_close(void) {
    free(format_buffers);
}

/**
 * Return a formatted string
 */
char* Util_format(char* format, ...) {
    va_list ap;
    va_start(ap, format);
    pthread_t pid = pthread_self();
    bool found = false;
    int i;
    
    for(i = 0; i < buffer_count; i++) {
        if(format_buffers[i].id == pid) {
            found = true;
            break;
        }
    }

    if(!found) {
        buffer_count++;
        format_buffers = realloc(format_buffers, buffer_count * sizeof(struct Buffer));
        format_buffers[buffer_count - 1].id = pid;
    }

    /* Do the formatting */
    vsnprintf(format_buffers[i].buff, FORMAT_BUFF_SIZE, format, ap);
    va_end(ap);

    /* Return the formatted result */
    return format_buffers[i].buff;
}

/**
 * Sleep for s seconds 
 */
void Util_usleep(double s) {
    /* Construct a timespec object with the length of time taken from s */
    struct timespec ts;
    ts.tv_sec = (int)s;
    ts.tv_nsec = (s - ts.tv_sec) * 1e9;

    /* Do the sleep */
    nanosleep(&ts, NULL);
}

/**
 * Strip leading and trailing whitespace from a string. Strip is done in place
 */
void Util_strip(char* buffer) {
    int i, start;

    /* Skip empty strings */
    if(buffer[0] == '\0') {
        return;
    }

    /* Work forward in the string until we find a non blank character */
    for(start = 0; isspace(buffer[start]); start++);

    /* Move string starting with first non blank character to the beginning of
       the buffer */
    for(i = 0; buffer[start + i] != '\0'; i++) {
        buffer[i] = buffer[start + i];
    }
    buffer[i--] = '\0';

    /* Work backwards from the end of the buffer until we reach a non blank
       character */
    while(isspace(buffer[i])) {
        /* Override each space with a null terminator */
        buffer[i--] = '\0';
    }
}

/**
 * Split the string buffer at the first occurence of the character split and
 * store the two parts in p1 and p2
 */
int Util_split(const char* buffer, char split, char* p1, char* p2) {
    int i, j;

    /* Copy characters from the buffer into p1 until we get to the split
       character */
    for(i = 0; buffer[i] != split; i++) {
        p1[i] = buffer[i];

        /* Didn't find the split character */
        if(buffer[i] == '\0') {
            return 1;
        }
    }
    p1[i] = '\0'; /* Terminate p1 */

    /* Copy from buffer, starting with the next character after the split
       character, into p2 until the end of buffer */
    for(j = 0; buffer[i + j + 1] != '\0'; j++) {
        p2[j] = buffer[i + j + 1];
    }
    p2[j] = '\0'; /* Terminate p2 */

    return 0;
}
