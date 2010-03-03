/**
 * \file
 * \brief Shared variable support
 */

#include "seawolf.h"

/** If true, then notications are sent out with variable updates */
static bool notify = true;

/**
 * \defgroup Var Shared variable
 * \ingroup Communications
 * \brief Provides functions for setting and retrieving shared variables
 * \{
 */

/**
 * \brief Get a variable
 *
 * Get the value of a variable
 *
 * \param name The variable to retrieve
 * \return The variable value
 */
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

/**
 * \brief Set a variable
 *
 * Set a variable to a given value
 *
 * \param name Variable to set
 * \param value Value to set the variable to
 */
void Var_set(char* name, float value) {
    static char* namespace = "VAR";
    static char* command = "SET";
    
    Comm_Message* variable_set = Comm_Message_new(4);

    variable_set->components[0] = namespace;
    variable_set->components[1] = command;
    variable_set->components[2] = name;
    variable_set->components[3] = strdup(__Util_format("%.4f", value));

    Comm_sendMessage(variable_set);

    if(notify) {
        Notify_send("UPDATED", name);
    }

    free(variable_set->components[3]);
    Comm_Message_destroy(variable_set);
}

/**
 * \brief Control auto-notifications
 *
 * If set to true then notifications in the form Notify_send("UPDATED", name)
 * will be sent every time a Var_set() call is made. If false then no such
 * notifications will be automatically set.
 *
 * \param autonotify If true, notifications are sent whenever Var_set is
 * called. If false, no notifications are sent
 */
void Var_setAutoNotify(bool autonotify) {
    notify = autonotify;
}

/** \} */
