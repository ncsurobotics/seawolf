
#ifndef __SEAWOLF_HUB_INCLUDE_H
#define __SEAWOLF_HUB_INCLUDE_H

#include <sqlite3.h>

#define MAX_CLIENTS 128
#define MAX_ERRORS 8
#define COMM_PORT ((uint16_t)31427)

#define RESPOND_TO_NONE 0
#define RESPOND_TO_SENDER 1
#define RESPOND_TO_ALL 2
#define SHUTDOWN_SENDER 3

struct Hub_Var_s {
    char* name;
    double value;
    double default_value;
    bool persistent;
    bool readonly;
};

typedef struct Hub_Var_s Hub_Var;

typedef sqlite3 Hub_DB_Handle;
typedef sqlite3_stmt Hub_DB_Result;

void Hub_exitError(void);
void Hub_Net_mainLoop(void);
int Hub_Process_process(Comm_Message* message, Comm_Message** response, bool* authenticated);
char* Hub_Config_getOption(const char* config_key);

void Hub_DB_init(void);
void Hub_DB_setFile(const char* file);
Hub_DB_Result* Hub_DB_exec(const char* sql);
int Hub_DB_next(Hub_DB_Result* result);
void Hub_DB_freeResult(Hub_DB_Result* result);
double Hub_DB_getDouble(Hub_DB_Result* result, int col);
int Hub_DB_getInt(Hub_DB_Result* result, int col);
const char* Hub_DB_getString(Hub_DB_Result* result, int col);
void Hub_DB_close(void);

void Hub_Var_init(void);
Hub_Var* Hub_Var_get(const char* name);
int Hub_Var_set(const char* name, double value);
void Hub_Var_close(void);

void Hub_Logging_init(void);
void Hub_Logging_log(short log_level, char* msg);
void Hub_Logging_logWithName(char* app_name, short log_level, char* msg);
void Hub_Logging_close(void);

#endif // #ifndef __SEAWOLF_HUB_INCLUDE_H
