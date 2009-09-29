
#ifndef __SEAWOLF_NOTIFY_INCLUDE_H
#define __SEAWOLF_NOTIFY_INCLUDE_H

/* Hardcode max message length for simplicities sake */
#define MAX_MESSAGE_LENGTH 256

/* IO Modes */
#define NOTIFY_NET   0x01
#define NOTIFY_STDIO 0x02

/* Filter types */
#define FILTER_MATCH 0x01
#define FILTER_ACTION 0x02
#define FILTER_PREFIX 0x03

/* Repeater listening port */
#define NET_PORT ((unsigned short)31427)

/* System control methods */
void Notify_init();
void Notify_close();
void Notify_setMode(int mode);                /* Read/write messages to from the given source */
void Notify_setServer(char* hostname);        /* Set the name of the repeater server */

/* Public access methods */
void Notify_getRaw(char* message);
void Notify_get(char* action, char* param);   /* Read a the next message and store the components in msgname and param */

void Notify_sendRaw(char* message);
void Notify_send(char* action, char* param);  /* Messages are sent in the form MSGNAME param. Example, "UPDATED Depth", meaning that the variable Depth has been updated */

/* Filter messages, NULL filter to clear filters */
void Notify_filter(int filter_type, char* filter);

#endif // #ifndef __SEAWOLF_NOTIFY_INCLUDE_H
