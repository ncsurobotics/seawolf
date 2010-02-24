
#include "seawolf.h"
#include "seawolf_hub.h"

#include <sqlite3.h>

static sqlite3* db_handle = NULL;
static char* db_file = NULL;

void Hub_DB_init(void) {
    sqlite3_open(db_file, &db_handle);
    Hub_DB_exec("CREATE TABLE IF NOT EXISTS config (option VARCHAR PRIMARY KEY, value VARCHAR);");
    Hub_DB_exec("CREATE TABLE IF NOT EXISTS variables (id INT AUTO_INCREMENT UNIQUE PRIMARY KEY, time TIMESTAMP, precisetime DOUBLE, name CHAR(20), value FLOAT);");
    Hub_DB_exec("CREATE TABLE IF NOT EXISTS variable_definitions (name CHAR(20), default_value DOUBLE, persistent BOOL, readonly BOOL);");
}

void Hub_DB_setFile(const char* file) {
    db_file = strdup(file);
}

Hub_DB_Result* Hub_DB_exec(const char* sql) {
    sqlite3_stmt* stmt;
    sqlite3_prepare_v2(db_handle, sql, -1, &stmt, NULL);
    if(Hub_DB_next(stmt) == false) {
        Hub_DB_freeResult(stmt);
        return NULL;
    }
    return stmt;
}

int Hub_DB_next(Hub_DB_Result* result) {
    if(sqlite3_step(result) == SQLITE_ROW) {
        return true;
    }
    return false;
}

void Hub_DB_freeResult(Hub_DB_Result* result) {
    sqlite3_finalize(result);
}

double Hub_DB_getDouble(Hub_DB_Result* result, int col) {
    return sqlite3_column_double(result, col);
}

int Hub_DB_getInt(Hub_DB_Result* result, int col) {
    return sqlite3_column_int(result, col);
}

const char* Hub_DB_getString(Hub_DB_Result* result, int col) {
    return (const char*) sqlite3_column_text(result, col);
}

void Hub_DB_close(void) {
    if(db_file) {
        free(db_file);
    }
    sqlite3_close(db_handle);
}
