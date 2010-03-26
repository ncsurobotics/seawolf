
#include "seawolf.h"
#include "seawolf_hub.h"

static Dictionary* var_cache = NULL;

static void Hub_Var_initPersistentValues(void) {
    List* variable_names = Dictionary_getKeys(var_cache);
    int count = List_getSize(variable_names);
    char* variable_name;
    Hub_Var* var;
    Hub_DB_Result* result;
    
    for(int i = 0; i < count; i++) {
        variable_name = List_get(variable_names, i);
        var = Dictionary_get(var_cache, variable_name);
        if(var->persistent) {
            result = Hub_DB_exec(Util_format("SELECT value FROM variables WHERE name='%s'", variable_name));
            if(result) {
                var->value = Hub_DB_getDouble(result, 0);
                Hub_DB_freeResult(result);
            } else {
                Hub_DB_exec(Util_format("INSERT INTO variables (name, value) VALUES('%s', %f);", variable_name, var->default_value));
            }
        }
    }
    List_destroy(variable_names);
}

static void Hub_Var_initCacheTable(void) {
    Hub_Var* var;
    Hub_DB_Result* result = Hub_DB_exec("SELECT name, default_value, persistent, readonly FROM variable_definitions");
    
    if(result == NULL) {
        Hub_Logging_log(WARNING, "No variables defined, but continuing anyway");
        return;
    }

    /* Build caching table */
    do {
        var = malloc(sizeof(Hub_Var));
        var->name = strdup(Hub_DB_getString(result, 0));
        var->default_value = Hub_DB_getDouble(result, 1);
        var->persistent = Hub_DB_getInt(result, 2);
        var->readonly = Hub_DB_getInt(result, 3);
        var->value = var->default_value;
        Dictionary_set(var_cache, var->name, var);
    } while(Hub_DB_next(result));
    Hub_DB_freeResult(result);
}

void Hub_Var_init(void) {
    var_cache = Dictionary_new();
    Hub_Var_initCacheTable();
    Hub_Var_initPersistentValues();
}

Hub_Var* Hub_Var_get(const char* name) {
    Hub_Var* var = Dictionary_get(var_cache, name);
    return var;
}

int Hub_Var_set(const char* name, double value) {
    Hub_Var* var = Dictionary_get(var_cache, name);
    if(var == NULL) {
        return -1;
    }

    if(var->readonly) {
        return -2;
    }

    var->value = value;
    if(var->persistent) {
        /* Variable is persistent, flush it to the database */
        Hub_DB_exec(Util_format("UPDATE variables SET value=%f WHERE name='%s'", value, name));
    }

    return 0;
}

void Hub_Var_close(void) {
    List* keys = Dictionary_getKeys(var_cache);
    int count = List_getSize(keys);
    char* key;
    Hub_Var* var;

    for(int i = 0; i < count; i++) {
        key = List_get(keys, i);
        var = Dictionary_get(var_cache, key);
        free(var->name);
        free(var);
    }

    List_destroy(keys);
    Dictionary_destroy(var_cache);
}
