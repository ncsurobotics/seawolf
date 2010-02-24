
#include "seawolf.h"

#include <sys/socket.h>
#include <arpa/inet.h>

static char* comm_server = NULL;
static uint16_t comm_port = 31427;
static char* auth_password = NULL;
static int comm_socket;

static Queue* queue_out = NULL;
static Dictionary* response_set = NULL;

static void Comm_authenticate(void);
static Comm_PackedMessage* Comm_receivePackedMessage(void);
static int Comm_receiveThread(void);

void Comm_init(void) {
    struct sockaddr_in addr;

    queue_out = Queue_new();
    response_set = Dictionary_new();

    /* Build connection address */
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr(comm_server);
    addr.sin_port = htons(comm_port);

    /* Create socket */
    comm_socket = socket(AF_INET, SOCK_STREAM, 0);
    if(comm_socket == -1) {
        Logging_log(CRITICAL, Util_format("Unable to create socket: %s", strerror(errno)));
        Seawolf_exitError();
    }

    /* Connect socket */
    if(connect(comm_socket, (struct sockaddr*) &addr, sizeof(addr))) {
        Logging_log(CRITICAL, Util_format("Unable to connect to Comm server: %s", strerror(errno)));
        Seawolf_exitError();
    }
    
    /* Run receive thread */
    Task_background(&Comm_receiveThread);

    /* Authenticate */
    Comm_authenticate();
}

static void Comm_authenticate(void) {
    static char* namespace = "COMM";
    static char* command = "AUTH";

    if(auth_password) {
        Comm_Message* auth_message = Comm_Message_new();
        Comm_Message* response;

        auth_message->count = 3;
        auth_message->components = malloc(sizeof(char*) * 3);
        auth_message->components[0] = namespace;
        auth_message->components[1] = command;
        auth_message->components[2] = auth_password;

        Comm_assignRequestID(auth_message);
        response = Comm_sendMessage(auth_message);

        if(strcmp(response->components[1], "SUCCESS") == 0) {
            Comm_Message_destroy(auth_message);
            free(response->components[0]);
            Comm_Message_destroy(response);
            return;
        } else {
            Logging_log(CRITICAL, "Unable to authenticate with comm server");
        }
    }
    
    Logging_log(CRITICAL, "No Comm_password set. Unable to connect to Comm server");
    Seawolf_exitError();
}

static Comm_PackedMessage* Comm_receivePackedMessage(void) {
    Comm_PackedMessage* packed_message = Comm_PackedMessage_new();
    uint16_t total_data_size;

    recv(comm_socket, &total_data_size, sizeof(uint16_t), MSG_WAITALL|MSG_PEEK);

    total_data_size = ntohs(total_data_size);
    packed_message->length = total_data_size + COMM_MESSAGE_PREFIX_LEN;
    packed_message->data = malloc(packed_message->length);

    recv(comm_socket, packed_message->data, packed_message->length, MSG_WAITALL);

    return packed_message;
}

static int Comm_receiveThread(void) {
    Comm_PackedMessage* packed_message;
    Comm_Message* message;

    while(true) {
        packed_message = Comm_receivePackedMessage();
        message = Comm_unpackMessage(packed_message);
        Comm_PackedMessage_destroy(packed_message);
        
        if(message->request_id != 0) {
            Dictionary_setInt(response_set, message->request_id, message);
        }
    }
}

Comm_Message* Comm_sendMessage(Comm_Message* message) {
    static pthread_mutex_t send_lock = PTHREAD_MUTEX_INITIALIZER;
    Comm_PackedMessage* packed_message = Comm_packMessage(message);
    Comm_Message* response = NULL;

    /* Send data */
    pthread_mutex_lock(&send_lock);
    send(comm_socket, packed_message->data, packed_message->length, 0);
    pthread_mutex_unlock(&send_lock);

    /* Destroy sent message */
    Comm_PackedMessage_destroy(packed_message);

    /* Expect a response and wait for it */
    if(message->request_id != 0) {
        Dictionary_waitForInt(response_set, message->request_id);
        response = Dictionary_getInt(response_set, message->request_id);
        Dictionary_removeInt(response_set, message->request_id);
    }
    
    return response;
}

void Comm_assignRequestID(Comm_Message* message) {
    static pthread_mutex_t request_id_lock = PTHREAD_MUTEX_INITIALIZER;
    static uint32_t last_id = 1;

    pthread_mutex_lock(&request_id_lock);
    message->request_id = last_id;
    last_id = (last_id + 1) % (1 << 16);
    pthread_mutex_unlock(&request_id_lock);
}

Comm_PackedMessage* Comm_packMessage(Comm_Message* message) {
    Comm_PackedMessage* packed_message = Comm_PackedMessage_new();
    size_t total_data_length = 0;
    size_t* component_lengths = malloc(sizeof(size_t) * message->count);
    char* buffer;
    int i;

    /* Add length of each message and space for a null terminator for each */
    for(i = 0; i < message->count; i++) {
        component_lengths[i] = strlen(message->components[i]) + 1;
        total_data_length += component_lengths[i];
    }

    /* Store message information */
    packed_message->length = sizeof(total_data_length) + COMM_MESSAGE_PREFIX_LEN;
    packed_message->data = malloc(packed_message->length);

    /* Build packed message header */
    ((uint16_t*)packed_message->data)[0] = htons(total_data_length);
    ((uint16_t*)packed_message->data)[1] = htons(message->request_id);
    ((uint16_t*)packed_message->data)[2] = htons(message->count);

    /* Copy message components */
    buffer = packed_message->data + COMM_MESSAGE_PREFIX_LEN;
    for(i = 0; i < message->count; i++) {
        memcpy(buffer, message->components[i], component_lengths[i]);
        buffer += component_lengths[i];
    }
    
    free(component_lengths);

    return packed_message;
}

Comm_Message* Comm_unpackMessage(Comm_PackedMessage* packed_message) {
    Comm_Message* message = Comm_Message_new();
    size_t data_length = ntohs(((uint16_t*)packed_message->data)[0]);

    /* Build message meta information */
    message->request_id = ntohs(((uint16_t*)packed_message->data)[1]);
    message->count = ntohs(((uint16_t*)packed_message->data)[2]);
    message->components = malloc(sizeof(char*) * message->count);

    /* Extract components -- we allocate all the space to the first and use the
       rest of the elements as indexes */
    message->components[0] = malloc(data_length);
    memcpy(message->components[0], packed_message->data + COMM_MESSAGE_PREFIX_LEN, data_length);

    /* Point the rest of the components into the space allocated to the first */
    for(int i = 1; i < message->count; i++) {
        message->components[i] = message->components[i-1] + strlen(message->components[i-1]) + 1;
    }

    return message;
}

Comm_Message* Comm_Message_new(void) {
    Comm_Message* message = malloc(sizeof(Comm_Message));
    
    message->request_id = 0;
    message->components = NULL;
    message->count = 0;

    return message;
}

Comm_PackedMessage* Comm_PackedMessage_new(void) {
    Comm_PackedMessage* packed_message = malloc(sizeof(Comm_PackedMessage));

    packed_message->length = 0;
    packed_message->data = NULL;

    return packed_message;
}

void Comm_Message_destroy(Comm_Message* message) {
    free(message->components);
    free(message);
}

void Comm_PackedMessage_destroy(Comm_PackedMessage* packed_message) {
    free(packed_message->data);
    free(packed_message);
}

void Comm_setPassword(const char* password) {
    auth_password = strdup(password);
}

void Comm_setServer(const char* server) {
    comm_server = strdup(server);
}

void Comm_setPort(uint16_t port) {
    comm_port = port;
}

void Comm_close(void) {
    Dictionary_destroy(response_set);
    Queue_destroy(queue_out);
    if(comm_server != NULL) {
        free(comm_server);
    }
}
