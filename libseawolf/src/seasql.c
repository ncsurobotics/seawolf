
#include "seawolf.h"

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

#include <mysql/mysql.h>

/* Make defining accessors easy */
#define MYSQL_ACCESSOR(name) float SeaSQL_get##name(void){return SeaSQL_getMostRecent(#name);} \
                             int SeaSQL_set##name(float value){return SeaSQL_updateVariable(#name, value);}

/* Define all variables and accessors */
MYSQL_ACCESSOR( SEA_Roll )
MYSQL_ACCESSOR( SEA_Yaw )
MYSQL_ACCESSOR( SEA_Pitch )
MYSQL_ACCESSOR( IEA_Roll )
MYSQL_ACCESSOR( IEA_Yaw )
MYSQL_ACCESSOR( IEA_Pitch )
MYSQL_ACCESSOR( IV_MagField_X )
MYSQL_ACCESSOR( IV_MagField_Y )
MYSQL_ACCESSOR( IV_MagField_Z )
MYSQL_ACCESSOR( IV_Accel_X )
MYSQL_ACCESSOR( IV_Accel_Y )
MYSQL_ACCESSOR( IV_Accel_Z )
MYSQL_ACCESSOR( IV_AngRate_X )
MYSQL_ACCESSOR( IV_AngRate_Y )
MYSQL_ACCESSOR( IV_AngRate_Z )
MYSQL_ACCESSOR( IOM_11 )
MYSQL_ACCESSOR( IOM_21 )
MYSQL_ACCESSOR( IOM_31 )
MYSQL_ACCESSOR( IOM_12 )
MYSQL_ACCESSOR( IOM_22 )
MYSQL_ACCESSOR( IOM_32 )
MYSQL_ACCESSOR( IOM_13 )
MYSQL_ACCESSOR( IOM_23 )
MYSQL_ACCESSOR( IOM_33 )

/* Depth and depth heading */
MYSQL_ACCESSOR( Depth )
MYSQL_ACCESSOR( DepthHeading )
MYSQL_ACCESSOR( Altitude )
MYSQL_ACCESSOR( AltitudeHeading )
MYSQL_ACCESSOR( YawHeading )

/* Set point tracker heading */
MYSQL_ACCESSOR( SetPoint_Theta )
MYSQL_ACCESSOR( SetPoint_Phi )
MYSQL_ACCESSOR( SetPoint_Rho )

/* Fake set points */
MYSQL_ACCESSOR( SetPointSource )
MYSQL_ACCESSOR( SetPointVision_Theta )
MYSQL_ACCESSOR( SetPointVision_Phi )
MYSQL_ACCESSOR( SetPointVision_Rho )
MYSQL_ACCESSOR( SetPointAcoustics_Theta )
MYSQL_ACCESSOR( SetPointAcoustics_Phi )
MYSQL_ACCESSOR( SetPointAcoustics_Rho )
MYSQL_ACCESSOR( SetPointOverride_Theta )
MYSQL_ACCESSOR( SetPointOverride_Phi )
MYSQL_ACCESSOR( SetPointOverride_Rho )

/* PID Tunables */
MYSQL_ACCESSOR( DepthPID_p )
MYSQL_ACCESSOR( DepthPID_i )
MYSQL_ACCESSOR( DepthPID_d )
MYSQL_ACCESSOR( AltitudePID_p )
MYSQL_ACCESSOR( AltitudePID_i )
MYSQL_ACCESSOR( AltitudePID_d )
MYSQL_ACCESSOR( RollPID_p )
MYSQL_ACCESSOR( RollPID_i )
MYSQL_ACCESSOR( RollPID_d )
MYSQL_ACCESSOR( PitchPID_p )
MYSQL_ACCESSOR( PitchPID_i )
MYSQL_ACCESSOR( PitchPID_d )
MYSQL_ACCESSOR( YawPID_p )
MYSQL_ACCESSOR( YawPID_i )
MYSQL_ACCESSOR( YawPID_d )

/* Thrusters */
MYSQL_ACCESSOR( Aft )
MYSQL_ACCESSOR( PortX )
MYSQL_ACCESSOR( PortY )
MYSQL_ACCESSOR( StarX )
MYSQL_ACCESSOR( StarY )

/* Vision information */
MYSQL_ACCESSOR( VisionTarget )
MYSQL_ACCESSOR( VisionFound )

/* Status */
MYSQL_ACCESSOR( MissionStatus )
MYSQL_ACCESSOR( CountDownStatus )

/* Depth controller */
MYSQL_ACCESSOR( TrackerDoDepth )
MYSQL_ACCESSOR( PIDDoYaw )

/* Pinger delays */
MYSQL_ACCESSOR( PingDelay_a )
MYSQL_ACCESSOR( PingDelay_b )
MYSQL_ACCESSOR( PingDelay_c )

/* SQL expressions used in queries */
#define UPDATEVAR_SQL "UPDATE variables SET time=NOW(), precisetime=%f, value=%8f WHERE name='%s';"
#define INSERTVAR_SQL "INSERT INTO variables VALUES(0, NOW(), %f, '%s', %8f);"
#define GETVAR_SQL "SELECT value FROM variables WHERE name='%s' ORDER BY id DESC LIMIT 1;"
#define CREATE_VAR_TABLE "CREATE TABLE IF NOT EXISTS variables (id INT AUTO_INCREMENT UNIQUE PRIMARY KEY, time TIMESTAMP, precisetime DOUBLE, name CHAR(20), value FLOAT);"

/* This is the SeaSQL configuration. These values can be changed with an
   appropriate call to on of the SeaSQL_config* functions */
static SeaSQL_config seasql_config = {"localhost",  /* System MySQL is running on */
                                      "root",       /* MySQL user */
                                      "",           /* Password corresponding with the username */
                                      "seasql",     /* Default database name */
                                      3306 };       /* Default MySQL port, should not change */

/* Global MySQL connection object */
static MYSQL* mysql_conn = NULL;
static bool notify = true;

/* MySQL call mutex */
static pthread_mutex_t* mysql_lock = NULL;

/**
 * Set the hostname to use for the MySQL server
 */
void SeaSQL_setServer(const char* hostname) {
    strcpy(seasql_config.hostname, hostname);
}

/**
 * Set the username for the MySQL server
 */
void SeaSQL_setUsername(const char* username) {
    strcpy(seasql_config.username, username);
}

/**
 * Set the password for the MySQL server
 */
void SeaSQL_setPassword(const char* password) {
    strcpy(seasql_config.password, password);
}

/**
 * Set the database to connect to
 */
void SeaSQL_setDatabase(const char* db_name) {
    strcpy(seasql_config.database, db_name);
}

/**
 * Set the port to connect to for the MySQL server
 */
void SeaSQL_setPort(unsigned short port) {
    seasql_config.port = port;
}

/**
 * Initialize SeaSQL and connect to MySQL 
 */
void SeaSQL_init(void) {
    /* This can be manually called or will be automatically called on first 
       attempted function call */

    /* Intialize lock and specify that recursion is allowable */
    mysql_lock = malloc(sizeof(pthread_mutex_t));
    pthread_mutexattr_t attr;
    pthread_mutexattr_init(&attr);
    pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_RECURSIVE);
    pthread_mutex_init(mysql_lock, &attr);
    pthread_mutexattr_destroy(&attr);

    /* Initialize and connect */
    mysql_conn = mysql_init(NULL);
    if(mysql_real_connect(mysql_conn, 
                          seasql_config.hostname,  /* Configuration options */
                          seasql_config.username,
                          seasql_config.password,
                          seasql_config.database,
                          seasql_config.port,
                          NULL, 0)) {
        /* Create variables table */
        SeaSQL_execute(CREATE_VAR_TABLE);
        return;
    }

    /* Unable to connect, display an error message and then exit */
    fprintf(stderr, "Error connecting to MySQL database: %s\nExiting\n", mysql_error(mysql_conn));
    exit(1);
}

/**
 * Close SeaSQL component. Disconnect from MySQL 
 */
void SeaSQL_close(void) {
    /* Destroy and free lock and disconnect from MySQL */
    pthread_mutex_destroy(mysql_lock);
    free(mysql_lock);
    mysql_close(mysql_conn);
    mysql_library_end();
    mysql_conn = NULL;
}

/**
 * Execute a SQL expression
 */
int SeaSQL_execute(char* cmd) {
    int return_value;
    pthread_mutex_lock(mysql_lock);
    return_value = mysql_query(mysql_conn, cmd);
    if(return_value) {
        /* Error occured, print error to standard error */
        fprintf(stderr, "SeaSQL Error on expression \"%s\": %s\n", cmd, mysql_error(mysql_conn));
    }
    pthread_mutex_unlock(mysql_lock);
    return return_value;
}

/**
 * SeaSQL variable updates should send notify messages out automatically
 */
void SeaSQL_setAutoNotify(bool do_notify) {
    notify = do_notify;
}

/**
 * Update a variable value
 */
int SeaSQL_updateVariable(char* name, float value) {
    /* Compute high precision timestamp */
    double precisetime;
    struct timespec now;
    clock_gettime(CLOCK_REALTIME, &now);
    precisetime = (double) now.tv_sec + ((double) now.tv_nsec / 1e9);

    /* Execute update var statement */
    SeaSQL_execute(Util_format(UPDATEVAR_SQL, precisetime, value, name));

    /* Variable does not exist to update -- insert it */
    if(mysql_affected_rows(mysql_conn) == 0) {
        SeaSQL_execute(Util_format(INSERTVAR_SQL, precisetime, name, value));
    }

    /* Send the update notification */
    if(notify) {
        Notify_send("UPDATED", name);
    }

    return 0;
}

/**
 * Get most recent value of the given variable
 */
float SeaSQL_getMostRecent(char* name) {
    pthread_mutex_lock(mysql_lock);

    MYSQL_RES* result;
    MYSQL_ROW row;
    float value;

    /* Format and run commands */
    SeaSQL_execute(Util_format(GETVAR_SQL, name));

    /* Retrieve result set */
    result = mysql_store_result(mysql_conn);
    if(mysql_num_rows(result) == 0) {
        /* No rows found so return -1 */
        value = -1.0;
    } else {
        row = mysql_fetch_row(result);
        value = atof(row[0]);
    }

    mysql_free_result(result);
    pthread_mutex_unlock(mysql_lock);

    return value;
}

/**
 * Purge records from the variables table
 */
void SeaSQL_clearVariables(void) {
    /* Drop all values and reset autoincrement */
    pthread_mutex_lock(mysql_lock);
    SeaSQL_execute("DELETE FROM variables;");
    SeaSQL_execute("ALTER TABLE variables AUTO_INCREMENT=1;");
    pthread_mutex_unlock(mysql_lock);
}

