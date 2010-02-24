
#include "seawolf.h"

static bool notify = true;

void Var_init(void) {
    // --
}

float Var_get(char* name) {
    static char* namespace = "VAR";
    static char* command = "GET";

    Comm_Message* variable_request = Comm_Message_new(3);
    Comm_Message* response;
    float value;

    variable_request->components[0] = namespace;
    variable_request->components[1] = command;
    variable_request->components[2] = name;
    
    Comm_assignRequestID(variable_request);
    response = Comm_sendMessage(variable_request);

    value = atof(response->components[2]);
    Comm_Message_destroyUnpacked(response);
    Comm_Message_destroy(variable_request);

    return value;
}

void Var_set(char* name, float value) {
    static char* namespace = "VAR";
    static char* command = "SET";
    
    Comm_Message* variable_set = Comm_Message_new(4);

    variable_set->components[0] = namespace;
    variable_set->components[1] = command;
    variable_set->components[2] = name;
    variable_set->components[3] = strdup(Util_format("%.4f", value));

    Comm_sendMessage(variable_set);

    if(notify) {
        Notify_send("UPDATED", name);
    }

    free(variable_set->components[3]);
    Comm_Message_destroy(variable_set);
}

void Var_setAutoNotify(bool autonotify) {
    notify = autonotify;
}

void Var_close(void) {
    // --
}
