
#ifndef __SEAWOLF_SEASQLCONFIG_INCLUDE_H
#define __SEAWOLF_SEASQLCONFIG_INCLUDE_H

struct SeaSQL_config_s {
    /* This is easier */
    char hostname[64];
    char username[64];
    char password[64];
    char database[64];
    int port;
};

typedef struct SeaSQL_config_s SeaSQL_config;

/* Load the configuration from a configuration file */
void SeaSQL_configFile(char* filename);

/* Prompt for all configuration values and create a config through this */
void SeaSQL_configPrompt(void);

/* Retrieve the configuration object */
SeaSQL_config* SeaSQL_getConfig(void);

#endif // #ifndef __SEAWOLF_SEASQLCONFIG_INCLUDE_H
