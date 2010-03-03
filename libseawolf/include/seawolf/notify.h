/**
 * \file
 */

#ifndef __SEAWOLF_NOTIFY_INCLUDE_H
#define __SEAWOLF_NOTIFY_INCLUDE_H

#include "comm.h"

/**
 * Match the filter on the whole message
 */
#define FILTER_MATCH 0x01

/**
 * Match the filter on the message action
 */
#define FILTER_ACTION 0x02

/**
 * Match the filter on some prefix of the message
 */
#define FILTER_PREFIX 0x03

/**
 * If no filters are registered, default to accepting messages
 */
#define NOTIFY_POLICY_ACCEPT true

/**
 * If no filters are registered, default to dropping messages
 */
#define NOTIFY_POLICY_DROP false

/* System control methods */
void Notify_init(void);
void Notify_close(void);
void Notify_setPolicy(bool policy);

/* Called to insert a new message into the input queue */
void Notify_inputMessage(Comm_Message* message);

/* Public access methods */
void Notify_get(char* action, char* param);
void Notify_send(char* action, char* param);

/* Filter messages, NULL filter to clear filters */
void Notify_filter(int filter_type, char* filter);

#endif // #ifndef __SEAWOLF_NOTIFY_INCLUDE_H
