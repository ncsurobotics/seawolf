/**
 * \file
 * \brief Misc utilities
 */

#include "seawolf.h"

#include <pthread.h>
#include <stdarg.h>
#include <ctype.h>
#include <time.h>
#include <sys/time.h>

/**
 * A format buffer for a particular thread
 */
struct Buffer {
    /**
     * Thread ID of the owner of this buffer
     */
    pthread_t id;

    /**
     * The format buffer
     */
    char* buff;

    /**
     * The format buffer size
     */
    size_t size;
};

/** Format buffers for client */
static struct Buffer* format_buffers = NULL;

/** Number of format buffers for client */
static int buffer_count = 0;

/** Format buffers for internal libseawolf use */
static struct Buffer* format_buffers_internal = NULL;

/** Number of format buffers for libseawolf */
static int buffer_count_internal = 0;

/**
 * \defgroup Util Misc
 * \ingroup Utilities
 * \brief Utility functions
 * \{
 */

/**
 * \brief Format a string
 *
 * Format a string as sprintf, but return the buffer rather than needing one
 * provided. The returned value should *not* be passed to free and the space
 * will be reused on the next call to Util_format(). This function is thread
 * safe however, and every thread has its own buffer.
 *
 * \param format Format string as in sprintf
 * \param ... Arguments to the format string
 * \return The formatted string
 */
char* Util_format(char* format, ...) {
    va_list ap;
    va_start(ap, format);
    pthread_t pid = pthread_self();
    bool found = false;
    size_t length;
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
        format_buffers[buffer_count - 1].size = 0;
        format_buffers[buffer_count - 1].buff = NULL;
    }

    /* Do the formatting */
    length = vsnprintf(format_buffers[i].buff, format_buffers[i].size, format, ap);
    if(length >= format_buffers[i].size) {
        /* Buffer wasn't large enough, resize */
        format_buffers[i].size = length + 1;
        format_buffers[i].buff = realloc(format_buffers[i].buff, sizeof(char) * format_buffers[i].size);

        /* Reformat */
        va_start(ap, format);
        vsnprintf(format_buffers[i].buff, format_buffers[i].size, format, ap);
    }
    va_end(ap);

    /* Return the formatted result */
    return format_buffers[i].buff;
}

/**
 * \private
 * \sa Util_format
 *
 * \param format Format string as in sprintf
 * \param ... Arguments to the format string
 * \return The formatted string
 */
char* __Util_format(char* format, ...) {
    va_list ap;
    va_start(ap, format);
    pthread_t pid = pthread_self();
    bool found = false;
    size_t length;
    int i;
    
    for(i = 0; i < buffer_count_internal; i++) {
        if(format_buffers_internal[i].id == pid) {
            found = true;
            break;
        }
    }

    if(!found) {
        buffer_count_internal++;
        format_buffers_internal = realloc(format_buffers_internal, buffer_count_internal * sizeof(struct Buffer));
        format_buffers_internal[buffer_count_internal - 1].id = pid;
        format_buffers_internal[buffer_count_internal - 1].size = 0;
        format_buffers_internal[buffer_count_internal - 1].buff = NULL;
    }

    /* Do the formatting */
    length = vsnprintf(format_buffers_internal[i].buff, format_buffers_internal[i].size, format, ap);
    if(length >= format_buffers_internal[i].size) {
        /* Buffer wasn't large enough, resize */
        format_buffers_internal[i].size = length + 1;
        format_buffers_internal[i].buff = realloc(format_buffers_internal[i].buff, sizeof(char) * format_buffers_internal[i].size);

        /* Reformat */
        va_start(ap, format);
        vsnprintf(format_buffers_internal[i].buff, format_buffers_internal[i].size, format, ap);
    }
    va_end(ap);

    /* Return the formatted result */
    return format_buffers_internal[i].buff;
}

/**
 * \brief Sleep
 *
 * Pause for s seconds
 *
 * \param s Seconds to sleep
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
 * \brief Strip a string of whitespace
 *
 * Strip leading and trailing whitespace from a string. This operation is done in place
 *
 * \param[in,out] buffer String buffer to perform operation on in place
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
 * \brief Split a string
 *
 * Split the string buffer at the first occurence of the character split and
 * store the two parts in p1 and p2
 *
 * \param buffer String the split
 * \param split Character to split by
 * \param[out] p1 Buffer to write the part before the split
 * \param[out] p2 Buffer to write the part after the split
 * \return 0 if successful, 1 if the split character is unfound
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

/**
 * \brief Close the Util component
 * \private
 */
void Util_close(void) {
    for(int i = 0; i < buffer_count; i++) {
        if(format_buffers[i].buff) {
            free(format_buffers[i].buff);
        }
    }
    free(format_buffers);

    for(int i = 0; i < buffer_count_internal; i++) {
        if(format_buffers_internal[i].buff) {
            free(format_buffers_internal[i].buff);
        }
    }
    free(format_buffers_internal);
}

/** \} */
