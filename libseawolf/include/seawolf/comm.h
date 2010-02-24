 
#ifndef __SEAWOLF_COMM_INCLUDE_H
#define __SEAWOLF_COMM_INCLUDE_H

/* A message has a request id (or zero for no request expected) and a number of
   components ASCII encoded */
struct Comm_Message_s {
    uint16_t request_id;
    char** components;
    unsigned short count;
};

/* The packed message format is quite simple,

   length           [0:15]
   request id       [16:31]
   component count  [32:47]
   data             [48:48 + length]
     component 1 \0
     component 2 \0
     ...

   Binary prefix and the data is assumed to be ASCII encoded data with
   components separated by null characters
*/
struct Comm_PackedMessage_s {
    uint16_t length; /* Total length, including prefix. This differs from
                        the length embedded in the packed message which
                        only includes the data length */
    char* data;
};

typedef struct Comm_Message_s Comm_Message;
typedef struct Comm_PackedMessage_s Comm_PackedMessage;

/* length, request id, component count */
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
