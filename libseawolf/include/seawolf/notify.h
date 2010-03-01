
#ifndef __SEAWOLF_NOTIFY_INCLUDE_H
#define __SEAWOLF_NOTIFY_INCLUDE_H

#include "comm.h"

/* Hardcode max message length for simplicities sake */
#define MAX_MESSAGE_LENGTH 256

/* Filter types */
#define FILTER_MATCH 0x01
#define FILTER_ACTION 0x02
#define FILTER_PREFIX 0x03

/* Policy */
#define NOTIFY_POLICY_ACCEPT true
#define NOTIFY_POLICY_DROP false

/* System control methods */
void Notify_init(void);
void Notify_close(void);
void Notify_setPolicy(bool policy);

/* Called to insert a new message into the input queue */
void Notify_inputMessage(Comm_Message* message);

/* Public access methods */
void Notify_get(char* action, char* param);   /* Read a the next message and store the components in msgname and param */
void Notify_send(char* action, char* param);  /* Messages are sent in the form MSGNAME param. Example, "UPDATED Depth", meaning that the variable Depth has been updated */

/* Filter messages, NULL filter to clear filters */
void Notify_filter(int filter_type, char* filter);

#endif // #ifndef __SEAWOLF_NOTIFY_INCLUDE_H
