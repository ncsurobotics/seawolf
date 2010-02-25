
#include "seawolf.h"
#include "seawolf_hub.h"

static int Hub_Process_comm(Comm_Message* message, Comm_Message** response, bool* authenticated) {
    char* supplied_password = NULL;
    const char* actual_password;

    if((*authenticated) || message->count != 3 || strcmp(message->components[1], "AUTH") != 0) {
        return RESPOND_TO_NONE;
    }

    actual_password = Hub_Config_getOption("password");
    supplied_password = message->components[2];

    if(actual_password == NULL) {
        Hub_Logging_log(ERROR, "No password set! Refusing to authenticate clients!");
        return RESPOND_TO_NONE;
    }

    *response = Comm_Message_new(2);
    (*response)->request_id = message->request_id;
    (*response)->components[0] = strdup("COMM");

    if(strcmp(supplied_password, actual_password) == 0) {
        (*response)->components[1] = strdup("SUCCESS");
        *authenticated = true;
    } else {
        Hub_Logging_log(INFO, __Util_format("Password: '%s'", actual_password));
        (*response)->components[1] = strdup("FAILURE");
    }

    free((char*)actual_password);

    return RESPOND_TO_SENDER;
}

static int Hub_Process_notify(Comm_Message* message, Comm_Message** response) {
    if(message->count != 3 || strcmp(message->components[1], "OUT") != 0) {
        return RESPOND_TO_NONE;
    }

    *response = Comm_Message_new(3);
    (*response)->components[0] = strdup("NOTIFY");
    (*response)->components[1] = strdup("IN");
    (*response)->components[2] = strdup(message->components[2]);

    return RESPOND_TO_ALL;
}

static int Hub_Process_log(Comm_Message* message, Comm_Message** response) {
    if(message->count != 4) {
        return RESPOND_TO_NONE;
    }

    Hub_Logging_logWithName(message->components[1], atoi(message->components[2]), message->components[3]);
    return RESPOND_TO_NONE;
}

static int Hub_Process_var(Comm_Message* message, Comm_Message** response) {
    if(message->count == 3 && strcmp(message->components[1], "GET") == 0) {
        *response = Comm_Message_new(3);
        (*response)->request_id = message->request_id;
        (*response)->components[0] = strdup("VAR");
        (*response)->components[1] = strdup("VALUE");
        (*response)->components[2] = strdup(__Util_format("%f", Hub_Var_get(message->components[2])));
        return RESPOND_TO_SENDER;
    } else if(message->count == 4 && strcmp(message->components[1], "SET") == 0) {
        Hub_Var_set(message->components[2], atof(message->components[3]));
    }
    return RESPOND_TO_NONE;
}

int Hub_Process_process(Comm_Message* message, Comm_Message** response, bool* authenticated) {
    int respond_to = RESPOND_TO_NONE;
    *response = NULL;

    if(strcmp(message->components[0], "COMM") == 0) {
        respond_to = Hub_Process_comm(message, response, authenticated);
    } else if(*authenticated) {
        if(strcmp(message->components[0], "NOTIFY") == 0) {
            respond_to = Hub_Process_notify(message, response);
        } else if(strcmp(message->components[0], "VAR") == 0) {
            respond_to = Hub_Process_var(message, response);
        } else if(strcmp(message->components[0], "LOG") == 0) {
            respond_to = Hub_Process_log(message, response);
        }
    }

    return respond_to;
}
