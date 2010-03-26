
#include "seawolf.h"
#include "seawolf_hub.h"

char* Hub_Config_getOption(const char* config_key) {
    Hub_DB_Result* result = Hub_DB_exec(Util_format("SELECT value FROM config WHERE option='%s'", config_key));
    char* value = NULL;

    if(result) {
        value = strdup(Hub_DB_getString(result, 0));
        Hub_DB_freeResult(result);
    }

    return value;
}
