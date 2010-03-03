/**
 * \file
 */
 
#ifndef __SEAWOLF_COMM_INCLUDE_H
#define __SEAWOLF_COMM_INCLUDE_H

/**
 * \brief An unpacked message
 *
 * The unpacked representation of a message. A message is associated with a
 * number of components consisting of ASCII text and request ID.
 */
typedef struct {
    /**
     * A request ID for the message. A hub always returns responses to requests
     * using the same ID as given in the request. In this way responses can be
     * paired with requests. The ID 0 is reserved for messages not expecting
     * responses 
     */
    uint16_t request_id;

    /**
     * The components of the message. Each component is an ASCII string
     */
    char** components;

    /**
     * The number of components in the message
     */
    unsigned short count;
} Comm_Message;

/**
 * \brief The packed representation of a message
 *
 * A messaged packed into a byte stream ready to be sent to the hub
 *
 * The packed message format is quite simple,<br>
 * <pre>
 *  length           [0:15]
 *  request id       [16:31]
 *  component count  [32:47]
 *  data             [48:48 + length]
 *    component 1 \\0
 *    component 2 \\0
 *    ...
 * </pre>
 *
 * The length, request ID, and component count constitute a 6 byte binary
 * header, and the rest of the message is null separated ASCII strings
 */
typedef struct {
    /**
     * Total length of the message including the 6 byte prefix
     */
    uint16_t length;

    /**
     * The packed message data
     */
    char* data;
} Comm_PackedMessage;

/**
 * Length of the binary header in all packed messages
 * \private
 */
#define COMM_MESSAGE_PREFIX_LEN (sizeof(uint16_t) * 3)

void Comm_init(void);
Comm_Message* Comm_sendMessage(Comm_Message* message);
void Comm_assignRequestID(Comm_Message* message);
Comm_PackedMessage* Comm_packMessage(Comm_Message* message);
Comm_Message* Comm_unpackMessage(Comm_PackedMessage* packed_message);
Comm_Message* Comm_Message_new(unsigned int component_count);
Comm_PackedMessage* Comm_PackedMessage_new(void);
void Comm_Message_destroy(Comm_Message* message);
void Comm_Message_destroyUnpacked(Comm_Message* message);
void Comm_PackedMessage_destroy(Comm_PackedMessage* packed_message);
void Comm_setPassword(const char* password);
void Comm_setServer(const char* server);
void Comm_setPort(uint16_t port);
void Comm_close(void);

#endif // #ifndef __SEAWOLF_COMM_INCLUDE_H
