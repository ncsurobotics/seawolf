
#include "seawolf.h"

void Var_init(void) {
    // --
}

float Var_get(char* name) {
    static char* namespace = "VAR";
    static char* command = "GET";

    Comm_Message* variable_request = Comm_Message_new();
    Comm_Message* response;
    float value;

    variable_request->count = 3;
    variable_request->components = malloc(sizeof(char*) * 3);
    variable_request->components[0] = namespace;
    variable_request->components[1] = command;
    variable_request->components[2] = name;
    
    Comm_assignRequestID(variable_request);
    response = Comm_sendMessage(variable_request);

    value = atof(response->components[2]);
    free(response->components[0]);
    Comm_Message_destroy(response);
    Comm_Message_destroy(variable_request);

    return value;
}

void Var_set(char* name, float value) {
    // --
}

void Var_close(void) {
    // --
}
